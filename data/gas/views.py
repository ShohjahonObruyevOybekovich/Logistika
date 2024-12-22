from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from data.gas.models import GasStation
from data.gas.serializers import GasStationListSerializer


class GasStationListCreateAPIView(ListCreateAPIView):

    serializer_class = GasStationListSerializer
    queryset = GasStation.objects.all()


class RetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = GasStationListSerializer
    queryset = GasStation.objects.all()
