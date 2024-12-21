
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

from .serializers import (
    GasPurchaseCreateseralizer,
    GasAnotherStationCreateseralizer,
    GasStationListserializer, GasStationCreateserializer, GasPurchaseListseralizer, GasAnotherListserializer)
from .models import GasStation,GasPurchase,Gas_another_station


class GasPurchaseCreateAPIView(CreateAPIView):
    queryset = GasPurchase.objects.all()
    serializer_class = GasPurchaseCreateseralizer
    permission_classes = (IsAuthenticated,)


class GasPurchaseListAPIView(ListAPIView):
    queryset = GasPurchase.objects.all()
    serializer_class = GasPurchaseListseralizer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        'purchased_volume',
        'payed_price_uzs',
        'payed_price_usd',
        'price_uzs',
        'price_usd',
        "station",
    ]
    ordering_fields = ['purchased_volume']
    search_fields = ['purchased_volume',
                     'payed_price_uzs',
            'payed_price_usd'
                     ]


class GasPurchaseUpdateAPIView(UpdateAPIView):
    queryset = GasPurchase.objects.all()
    serializer_class = GasPurchaseCreateseralizer
    permission_classes = (IsAuthenticated,)




class GasInventoryListAPIView(ListAPIView):
    queryset = GasStation.objects.all()
    serializer_class = GasStationListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['gas_volume','last_payment',]
    ordering_fields = ['last_gas_volume']
    search_fields = ['last_gas_volume','last_payment']



class GasStationCreateAPIView(CreateAPIView):
    queryset = GasStation.objects.all()
    serializer_class = GasStationCreateserializer
    permission_classes = (IsAuthenticated,)

class GasStationUpdateAPIView(UpdateAPIView):
    queryset = GasStation.objects.all()
    serializer_class = GasStationCreateserializer
    permission_classes = (IsAuthenticated,)


class GasStationDeleteAPIView(DestroyAPIView):
    queryset = GasStation.objects.all()
    permission_classes = (IsAuthenticated,)



class GasAnotherStationCreateAPIView(CreateAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherStationCreateseralizer
    permission_classes = (IsAuthenticated,)


class GasAnotherStationListAPIView(ListAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['purchased_volume','payed_price_uzs',
            'payed_price_usd',]
    search_fields = ['purchased_volume','payed_price_uzs',
            'payed_price_usd']
    ordering_fields = ['purchased_volume']

class GasAnotherStationUpdateAPIView(UpdateAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherStationCreateseralizer
    permission_classes = (IsAuthenticated,)

class GasAnotherStationDeleteAPIView(DestroyAPIView):
    queryset = Gas_another_station.objects.all()
    permission_classes = (IsAuthenticated,)



