from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView, get_object_or_404, CreateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Oil, Remaining_oil_quantity, OilREcycles, OilPurchase, Utilized_oil
from .serializers import (
    OilCreateseralizer,
    Remaining_oil_quantityserializer, RecycledOilSerializer, OilPurchaseSerializer, Utilized_oilSerializer
)


class OilCreateAPIView(ListCreateAPIView):
    queryset = Oil.objects.all().order_by("-created_at")
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)


class OilUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Oil.objects.all()
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)


class OilListAPIView(ListAPIView):
    queryset = Oil.objects.all().order_by("-created_at")
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)

    def get_paginated_response(self, data):
        return Response(data)


class RecycledOilListAPIView(CreateAPIView):
    queryset = OilREcycles.objects.all().order_by("-created_at")
    serializer_class = RecycledOilSerializer
    permission_classes = (IsAuthenticated,)



class RecycledOilUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OilREcycles.objects.all()
    serializer_class = RecycledOilSerializer
    permission_classes = (IsAuthenticated,)

class RecycleOilCARListAPIView(ListAPIView):
    serializer_class = RecycledOilSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Get the `car_id` from query parameters
        car_id = self.request.query_params.get("car_id")

        # Base queryset
        queryset = OilREcycles.objects.all().order_by("-created_at")

        # Filter by car_id if provided
        if car_id:
            queryset = queryset.filter(car__id=car_id)

        return queryset


class OilPurchasesListAPIView(CreateAPIView):
    serializer_class = OilPurchaseSerializer
    permission_classes = [IsAuthenticated]
    queryset = OilPurchase.objects.all().order_by("-created_at")

class OilPurchaseReadAPIView(ListAPIView):
    serializer_class = OilPurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the `car_id` from query parameters
        oil_id = self.request.query_params.get("oil_id")

        # Base queryset
        queryset = OilPurchase.objects.all().order_by("-created_at")

        if oil_id:
            queryset = queryset.filter(oil__id=oil_id)

        return queryset

class OilDetailAPIView(ListAPIView):
    """
    API view to fetch oil details including purchases, recycling, utilization history,
    and remaining oil quantity.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request,*args, **kwargs):
        oil = get_object_or_404(Oil, id=kwargs['pk'])
        utilizations = Utilized_oil.objects.all().order_by("-created_at")
        remaining_oil = Remaining_oil_quantity.objects.first()
        # Assuming you're fetching the first object

        data = {
            "oil_name": oil.oil_name,
            "oil_volume": oil.oil_volume,
            "remaining_oil_quantity": remaining_oil.oil_volume if remaining_oil else None,

            "utilizations": Utilized_oilSerializer(utilizations, many=True).data,
        }
        return Response(data)




class OilDetailListAPIView(ListAPIView):
    """
    API view to fetch oil details including purchases, recycling, utilization history,
    and remaining oil quantity.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        oil = get_object_or_404(Oil, id=kwargs['pk'])

        # Filter utilizations by oil ID
        utilizations = Utilized_oil.objects.all()  # Adjust 'oil' to match your field name

        # Fetch remaining oil quantity
        remaining_oil = Remaining_oil_quantity.objects.first()
        purchases = OilPurchase.objects.filter(oil=oil).order_by("-created_at")

        data = {
            "oil_name": oil.oil_name,
            "oil_volume": oil.oil_volume,
            "remaining_oil_quantity": remaining_oil.oil_volume if remaining_oil else None,
            "utilizations": Utilized_oilSerializer(utilizations, many=True).data,
            "purchases": OilPurchaseSerializer(purchases, many=True).data
        }
        return Response(data)

class RecycleListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]

    # serializer_class = RecycledOilSerializer
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        oil = get_object_or_404(Oil, id=pk)
        recycles = OilREcycles.objects.filter(oil=oil)
        data = {
            "oil_name": oil.oil_name,
            "recycles": [
                {
                    "id": recycle.id,
                    "amount": recycle.amount,
                    "car": recycle.car.name,
                    "remaining_oil": recycle.remaining_oil,
                    "updated_at": recycle.updated_at,
                }
                for recycle in recycles
            ],
        }
        return Response(data)


class OilPurchaseUpdateAPIView(RetrieveUpdateAPIView):
    queryset = OilPurchase.objects.all()
    serializer_class = OilPurchaseSerializer
    permission_classes = (IsAuthenticated,)




class UtilizedOilPurchaseListAPIView(ListCreateAPIView):
    queryset = Utilized_oil.objects.all().order_by("-created_at")
    serializer_class = Utilized_oilSerializer
    permission_classes = [IsAuthenticated]


class UtilizedOilPurchaseUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Utilized_oil.objects.all()
    serializer_class = Utilized_oilSerializer
    permission_classes = [IsAuthenticated]


class RemainingOilPurchaseListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # You can modify this method to filter or get data dynamically
        return Remaining_oil_quantity.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = Remaining_oil_quantityserializer(queryset, many=True)
        return Response(serializer.data)
