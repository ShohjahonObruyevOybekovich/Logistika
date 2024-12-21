
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
)
from rest_framework.permissions import IsAuthenticated

from .models import Route,Flight
from .serializers import (
    RouteSerializer,RouteCreateSerializer,FlightCreateserializer,FlightListserializer
)


class RouteCreateAPIView(CreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteCreateSerializer
    permission_classes = (IsAuthenticated,)


class RouteListAPIView(ListAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['start',"end",]
    ordering_fields = ['start']
    search_fields = ['start',"end",]


class RouteUpdateAPIView(UpdateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAuthenticated,)


class RouteDeleteAPIView(DestroyAPIView):
    queryset = Route.objects.all()
    permission_classes = (IsAuthenticated,)





class FlightCreateAPIView(CreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightCreateserializer
    permission_classes = (IsAuthenticated,)

class FlightListAPIView(ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['region',"city","car","driver","departure_date","arrival_date"]
    ordering_fields = ['car']
    search_fields = ['region',"city","car","driver","departure_date","arrival_date"]

class FlightUpdateAPIView(UpdateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightCreateserializer
    permission_classes = (IsAuthenticated,)

class FlightDeleteAPIView(DestroyAPIView):
    queryset = Flight.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FlightListserializer




