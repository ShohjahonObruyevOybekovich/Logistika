import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    ListAPIView
from rest_framework.permissions import IsAuthenticated

from data.flight.serializers import FlightListserializer, FlightListCReateserializer, FlightOrderedListserializer
from .models import Flight, Ordered


class FlightListAPIView(ListCreateAPIView):
    queryset = Flight.objects.all().order_by("-created_at")
    serializer_class = FlightListserializer
    permission_classes = [IsAuthenticated]


class FlightRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightListserializer
    permission_classes = [IsAuthenticated]


class FlightFilter(django_filters.FilterSet):
    car_id = django_filters.UUIDFilter(field_name='car__id', lookup_expr='exact')

    class Meta:
        model = Flight
        fields = ['car_id']


class FlightStatsAPIView(ListAPIView):
    serializer_class = FlightListCReateserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FlightFilter  # Use the filter class

    def get_queryset(self):
        car_id = self.kwargs.get('pk')
        if car_id:
            # Filter the queryset by car_id
            return Flight.objects.filter(car__id=car_id).order_by("-created_at")
        return Flight.objects.none()


class FlightHistoryAPIView(ListAPIView):
    serializer_class = FlightListCReateserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FlightFilter

    def get_queryset(self):
        driver_id = self.kwargs.get('pk')
        if driver_id:
            return Flight.objects.filter(driver__id=driver_id).order_by("-created_at")
        return Flight.objects.none()

class FlightHistoryStatsAPIView(ListAPIView):
    serializer_class = FlightListCReateserializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        flight_id = self.kwargs.get('pk')
        if flight_id:
            return Flight.objects.filter(id=flight_id).order_by("-created_at")
        return Flight.objects.none()

class FlightListNOPg(ListAPIView):
    serializer_class = FlightListCReateserializer
    permission_classes = (IsAuthenticated,)
    queryset = Flight.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            print(f"Response type: {type(response)}")  # Debugging
            return response

        serializer = self.get_serializer(queryset, many=True)
        response = Response(serializer.data)
        print(f"Response type: {type(response)}")  # Debugging
        return response




class FlightOrderedListAPIView(ListCreateAPIView):
    serializer_class = FlightOrderedListserializer
    queryset = Ordered.objects.all().order_by("-created_at")
    permission_classes = (IsAuthenticated,)


class FlightOrderedRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Ordered.objects.all()
    serializer_class = FlightOrderedListserializer
    permission_classes = (IsAuthenticated,)

