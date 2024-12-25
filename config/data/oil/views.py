from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView, get_object_or_404
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
    queryset = Oil.objects.all()
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)


class OilUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Oil.objects.all()
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)


class OilListAPIView(ListAPIView):
    queryset = Oil.objects.all()
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)

    def get_paginated_response(self, data):
        return Response(data)


class RecycledOilListAPIView(ListCreateAPIView):
    queryset = OilREcycles.objects.all()
    serializer_class = RecycledOilSerializer
    permission_classes = (IsAuthenticated,)


class RecycledOilUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OilREcycles.objects.all()
    serializer_class = RecycledOilSerializer
    permission_classes = (IsAuthenticated,)


class OilDetailAPIView(ListAPIView):
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
        purchases = OilPurchase.objects.filter(oil=oil)

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
        pk = kwargs.get('pk')  # Retrieve 'pk' from kwargs
        oil = get_object_or_404(Oil, id=pk)
        recycles = OilREcycles.objects.filter(oil=oil)
        data = {
            "oil_name": oil.oil_name,
            "recycles": [
                {
                    "id": recycle.id,
                    "amount": recycle.amount,
                    "car": recycle.car.name,  # Include car ID or other fields
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
    queryset = Utilized_oil.objects.all()
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
