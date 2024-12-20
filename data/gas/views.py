
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
)
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (GasInventoryListserializer,
                          GasPurchaseCreateseralizer,
                          GasAnotherStationCreateseralizer)
from .models import GasInventory,GasPurchase,Gas_another_station


class GasPurchaseCreateAPIView(CreateAPIView):
    queryset = GasPurchase.objects.all()
    serializer_class = GasPurchaseCreateseralizer
    permission_classes = (IsAuthenticated,)


class GasPurchaseListAPIView(ListAPIView):
    queryset = GasPurchase.objects.all()
    serializer_class = GasPurchaseCreateseralizer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['purchased_volume','paid_amount',
                        'gas_price',"station_name",]
    ordering_fields = ['purchased_volume']
    search_fields = ['purchased_volume','paid_amount']


class GasPurchaseUpdateAPIView(UpdateAPIView):
    queryset = GasPurchase.objects.all()
    serializer_class = GasPurchaseCreateseralizer
    permission_classes = (IsAuthenticated,)


class GasInventoryListAPIView(ListAPIView):
    queryset = GasInventory.objects.all()
    serializer_class = GasInventoryListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['remaining_gas_volume','remaining_payment',]
    ordering_fields = ['remaining_gas_volume']
    search_fields = ['remaining_gas_volume','remaining_payment']


class GasInventoryUpdateAPIView(UpdateAPIView):
    queryset = GasInventory.objects.all()
    serializer_class = GasInventoryListserializer
    permission_classes = (IsAuthenticated,)


class GasInventoryDeleteAPIView(DestroyAPIView):
    queryset = GasInventory.objects.all()
    serializer_class = GasInventoryListserializer
    permission_classes = (IsAuthenticated,)


class GasAnotherStationCreateAPIView(CreateAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherStationCreateseralizer
    permission_classes = (IsAuthenticated,)


class GasAnotherStationListAPIView(ListAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherStationCreateseralizer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['purchased_volume','paid_amount',]
    search_fields = ['purchased_volume','paid_amount']
    ordering_fields = ['purchased_volume']

class GasAnotherStationUpdateAPIView(UpdateAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherStationCreateseralizer
    permission_classes = (IsAuthenticated,)

class GasAnotherStationDeleteAPIView(DestroyAPIView):
    queryset = Gas_another_station.objects.all()
    permission_classes = (IsAuthenticated,)



