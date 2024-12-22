from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from data.gas.models import GasStation
from data.gas.serializers import GasStationListSerializer
from root.pagination import GlobalPagination


class GasStationListCreateAPIView(ListCreateAPIView):

    serializer_class = GasStationListSerializer
    queryset = GasStation.objects.all()
    pagination_class = GlobalPagination


class RetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = GasStationListSerializer
    queryset = GasStation.objects.all()
