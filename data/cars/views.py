# from rest_framework import generics
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
)
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from .models import Car


class CarCreateAPIView(CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarCreateSerializer
    # permission_classes = (IsAuthenticated,)


class CarsListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListserializer
    # permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['name','number','type_of_payment',
                        'with_trailer',"fuel_type","price_uzs","price_usd",
                        'distance_travelled']
    ordering_fields = ['number']
    search_fields = ['name']

class CarsList_no_pg_APIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListserializer
    # permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['name','number','type_of_payment',
                        'with_trailer',"fuel_type","price_uzs","price_usd",
                        'distance_travelled']
    ordering_fields = ['number']
    search_fields = ['name']

    def get_paginated_response(self, data):
        return Response(data)


class CarByIDAPIView(RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListserializer
    permission_classes = (IsAuthenticated,)




    def get_object(self):
        try:
            obj = self.get_queryset().get(pk=self.kwargs.get('pk'))  # Use 'pk' here
            self.check_object_permissions(self.request, obj)
            return obj
        except Car.DoesNotExist:
            raise NotFound("Car not found.")


class CarUpdateAPIView(UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListserializer
    permission_classes = (IsAuthenticated,)


