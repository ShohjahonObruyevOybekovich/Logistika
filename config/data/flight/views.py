from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, \
    ListAPIView
from rest_framework.permissions import IsAuthenticated

from data.flight.serializers import FlightListserializer, FlightSerializer

from .models import Flight


class FlightListAPIView(ListAPIView):

    queryset = Flight.objects.all()
    serializer_class = FlightListserializer
    permission_classes = [IsAuthenticated]

class FlightRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightListserializer
    permission_classes = [IsAuthenticated]


class FlightCreateAPIView(CreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

