from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from data.flight.serializers import FlightListserializer

from .models import Flight


class FlightListAPIView(ListCreateAPIView):

    queryset = Flight.objects.all()
    serializer_class = FlightListserializer
    permission_classes = [IsAuthenticated]

class FlightRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightListserializer
    permission_classes = [IsAuthenticated]

