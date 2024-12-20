
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
)
from rest_framework.permissions import IsAuthenticated

from .models import Salarka, Remaining_salarka_quantity
from .serializers import (
    SalarkaCreateseralizer,
    SalarkaListserializer,
Remaining_salarka_quantityserializer
)


class SalarkaCreateAPIView(CreateAPIView):
    queryset = Salarka.objects.all()
    serializer_class = SalarkaCreateseralizer
    permission_classes = (IsAuthenticated,)


class SalarkaListAPIView(ListAPIView):
    queryset = Salarka.objects.all()
    serializer_class = SalarkaListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['oil_volume',"oil_price",]
    ordering_fields = ['oil_volume']
    search_fields = ['oil_volume',"oil_price",]


class SalarkaUpdateAPIView(UpdateAPIView):
    queryset = Salarka.objects.all()
    serializer_class = SalarkaCreateseralizer
    permission_classes = (IsAuthenticated,)


class SalarkaDeleteAPIView(DestroyAPIView):
    queryset = Salarka.objects.all()
    permission_classes = (IsAuthenticated,)



class Remaining_salarka_quantityListAPIView(ListAPIView):
    queryset = Remaining_salarka_quantity.objects.all()
    serializer_class = Remaining_salarka_quantityserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['oil_volume']
    ordering_fields = ['oil_volume']
    search_fields = ["oil_volume"]



