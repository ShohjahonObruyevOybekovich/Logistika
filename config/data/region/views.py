from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import *
from .models import Region


class RegionListAPIVIew(ListCreateAPIView):

    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    # permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        "name",
    ]
    ordering_fields = ["-created_at"]
    search_fields = ["name"]


class RegionDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    # permission_classes = (IsAuthenticated,)
