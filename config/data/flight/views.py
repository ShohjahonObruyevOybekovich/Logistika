from rest_framework.generics import CreateAPIView, ListCreateAPIView

from config.data.flight.serializers import FlightListserializer

from .models import Flight


class FlightListAPIView(ListCreateAPIView):

    queryset = Flight.objects.all()
    serializer_class = FlightListserializer
