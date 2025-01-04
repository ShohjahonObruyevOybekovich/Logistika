from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response

from .models import Region
from .serializers import *


class RegionListAPIVIew(ListCreateAPIView):
    queryset = Region.objects.all().order_by("-created_at")
    serializer_class = RegionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        "name","flight_type"
    ]
    ordering_fields = ["-created_at"]
    search_fields = ["name","flight_type"]

class RegionPGListAPIVIew(ListAPIView):
    queryset = Region.objects.all().order_by("-created_at")
    serializer_class = RegionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        "name","flight_type"

    ]
    ordering_fields = ["-created_at"]
    search_fields = ["name","flight_type"]

    def get_paginated_response(self, data):
        return Response(data)


class RegionDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all().order_by("-created_at")
    serializer_class = RegionSerializer
