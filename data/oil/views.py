
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
)
from rest_framework.permissions import IsAuthenticated

from .models import Oil, Remaining_oil_quantity
from .serializers import (
    OilCreateseralizer,
    OilListserializer,
    Remaining_oil_quantityserializer
)


class OilCreateAPIView(CreateAPIView):
    queryset = Oil.objects.all()
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)


class OilListAPIView(ListAPIView):
    queryset = Oil.objects.all()
    serializer_class = OilListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['oil_name','oil_volume',
                        'paid_amount',"oil_price",]
    ordering_fields = ['oil_name']
    search_fields = ['oil_name','paid_amount']


class OilUpdateAPIView(UpdateAPIView):
    queryset = Oil.objects.all()
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)


class OilDeleteAPIView(DestroyAPIView):
    queryset = Oil.objects.all()
    permission_classes = (IsAuthenticated,)



class Remaining_oil_quantityListAPIView(ListAPIView):
    queryset = Remaining_oil_quantity.objects.all()
    serializer_class = Remaining_oil_quantityserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['oil_volume']
    ordering_fields = ['oil_volume']
    search_fields = ["oil_volume"]



