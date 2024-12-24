from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, \
    ListAPIView
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

#
# class FlightCreateAPIView(CreateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [IsAuthenticated]
import django_filters


class FlightFilter(django_filters.FilterSet):
    car_id = django_filters.UUIDFilter(field_name='car__id', lookup_expr='exact')

    class Meta:
        model = Flight
        fields = ['car_id']

class FlightStatsAPIView(ListAPIView):
    serializer_class = FlightListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FlightFilter  # Use the filter class

    def get_queryset(self):
        # Retrieve the 'pk' (car_id) from the URL kwargs
        car_id = self.kwargs.get('pk')
        if car_id:
            # Filter the queryset by car_id
            return Flight.objects.filter(car__id=car_id)
        return Flight.objects.none()

