from rest_framework.generics import CreateAPIView, ListCreateAPIView

from data.flight.serializers import FlightListserializer

from .models import Flight


class FlightListAPIView(ListCreateAPIView):

    queryset = Flight.objects.all()
    serializer_class = FlightListserializer
