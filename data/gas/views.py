from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from data.gas.models import GasStaion
from data.gas.serializers import GasStationListSerializer


class GasStationListCreateAPIView(ListCreateAPIView):

    serializer_class = GasStationListSerializer
    queryset = GasStaion.objects.all()


class RetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = GasStationListSerializer
    queryset = GasStaion.objects.all()
