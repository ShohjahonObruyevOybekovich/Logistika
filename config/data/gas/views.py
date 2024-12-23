from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, \
    DestroyAPIView, UpdateAPIView

from rest_framework.exceptions import NotFound

from data.gas.models import GasPurchase, GasSale, GasStation
from data.gas.serializers import (
    GasPurchaseListseralizer,
    GasSaleListseralizer,
    GasStationListSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from root.pagination import GlobalPagination

from data.gas.models import Gas_another_station
from data.gas.serializers import GasAnotherStationCreateseralizer, GasAnotherListserializer


class GasStationListCreateAPIView(ListCreateAPIView):

    serializer_class = GasStationListSerializer
    queryset = GasStation.objects.all()
    pagination_class = GlobalPagination


class RetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = GasStationListSerializer
    queryset = GasStation.objects.all()


class GasPurchasesListAPIView(ListCreateAPIView):

    serializer_class = GasPurchaseListseralizer

    def get_queryset(self):

        station = GasStation.objects.filter(pk=self.kwargs["pk"]).first()

        if not station:
            return GasPurchase.objects.none()

        return station.purchases.all()

    def perform_create(self, serializer):

        station = GasStation.objects.filter(pk=self.kwargs["pk"]).first()

        if not station:
            raise NotFound("Gas station not found.")

        serializer.save(station=station)


class GasSalesListAPIView(ListCreateAPIView):

    serializer_class = GasSaleListseralizer

    def get_queryset(self):

        station = GasStation.objects.filter(pk=self.kwargs["pk"]).first()

        if not station:
            return GasSale.objects.none()

        return station.sales.all()

    def perform_create(self, serializer):

        station = GasStation.objects.filter(pk=self.kwargs["pk"]).first()

        if not station:
            raise NotFound("Gas station not found.")

        serializer.save(station=station)



class GasAnotherStationCreateAPIView(CreateAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherStationCreateseralizer
    permission_classes = (IsAuthenticated,)


class GasAnotherStationListAPIView(ListAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["car",'purchased_volume','payed_price_uzs',
            'payed_price_usd',]
    search_fields = ['purchased_volume','payed_price_uzs',
            'payed_price_usd']
    ordering_fields = ['purchased_volume']

class GasAnotherStationnopgListAPIView(ListAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['purchased_volume','payed_price_uzs',
            'payed_price_usd',]
    search_fields = ['purchased_volume','payed_price_uzs',
            'payed_price_usd']
    ordering_fields = ['purchased_volume']
    def get_paginated_response(self, data):
        return Response(data)


class GasAnotherStationUpdateAPIView(UpdateAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherStationCreateseralizer
    permission_classes = (IsAuthenticated,)

class GasAnotherStationDeleteAPIView(DestroyAPIView):
    queryset = Gas_another_station.objects.all()
    permission_classes = (IsAuthenticated,)
