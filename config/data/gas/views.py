from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework.exceptions import NotFound

from data.gas.models import GasPurchase, GasSale, GasStation
from data.gas.serializers import (
    GasPurchaseListseralizer,
    GasSaleListseralizer,
    GasStationListSerializer,
)
from root.pagination import GlobalPagination


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
