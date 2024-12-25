from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated

from .models import Salarka, Sale
from .serializers import (
    SalarkaCreateseralizer, SaleSerializer, SalarkaListSerializer
)


class SalarkaCreateAPIView(CreateAPIView):
    queryset = Salarka.objects.all()
    serializer_class = SalarkaCreateseralizer
    permission_classes = (IsAuthenticated,)


class SalarkaListAPIView(ListAPIView):
    queryset = Salarka.objects.all().order_by("-created_at")
    serializer_class = SalarkaListSerializer
    permission_classes = (IsAuthenticated,)


class SalarkaUpdateAPIView(UpdateAPIView):
    queryset = Salarka.objects.all()
    serializer_class = SalarkaCreateseralizer
    permission_classes = (IsAuthenticated,)


class SalarkaDeleteAPIView(DestroyAPIView):
    queryset = Salarka.objects.all()
    permission_classes = (IsAuthenticated,)


class SaleCreateAPIView(ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = (IsAuthenticated,)


class SaleRetrieveAPIView(RetrieveAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


import django_filters


class SalarkaFilter(django_filters.FilterSet):
    car_id = django_filters.UUIDFilter(field_name='car__id', lookup_expr='exact')

    class Meta:
        model = Salarka
        fields = ['car_id']


class SalarkaStatsAPIView(ListAPIView):
    serializer_class = SalarkaCreateseralizer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SalarkaFilter  # Use the filter class

    def get_queryset(self):
        # Retrieve the 'pk' (car_id) from the URL kwargs
        car_id = self.kwargs.get('pk')
        if car_id:
            # Filter the queryset by car_id
            return Salarka.objects.filter(car__id=car_id)
        return Salarka.objects.none()
