from uuid import UUID

from django.contrib.admin.templatetags.admin_list import pagination
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView, get_object_or_404
)
from rest_framework.pagination import PageNumberPagination
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



class OilPurchasesListAPIView(ListCreateAPIView):

    serializer_class = OilPurchaseSerializer
    permission_classes = [IsAuthenticated]
    queryset = OilPurchase.objects.all()


class OilDetailAPIView(ListAPIView):
    """
    API view to fetch oil details including purchases, recycling, utilization history,
    and remaining oil quantity.
    """
    permission_classes = [IsAuthenticated]

    def get(self, **kwargs,):
        oil = get_object_or_404(Oil, id=kwargs['id'])
        utilizations = Utilized_oil.objects.all()
        remaining_oil = Remaining_oil_quantity.get()


        data = {
            "oil_name": oil.oil_name,
            "oil_volume": oil.oil_volume,
            "remaining_oil_quantity": remaining_oil.oil_volume,
            "utilizations": Utilized_oilSerializer(utilizations, many=True).data,
        }
        return Response(data)


class RecycleListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
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
                    "updated_at" : recycle.updated_at,
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
