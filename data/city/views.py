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
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from .models import City, Region


class CityCreateAPIView(CreateAPIView):
    queryset = City.objects.all()
    serializer_class = CityCreateSerializer
    permission_classes = (IsAuthenticated,)

class CityUpdateAPIView(UpdateAPIView):
    queryset = City.objects.all()
    serializer_class = CityCreateSerializer
    permission_classes = (IsAuthenticated,)


class CityListAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        'name','region',
        ]
    ordering_fields = ['name']
    search_fields = ['name','region']

class CityDeleteAPIView(DestroyAPIView):
    queryset = City.objects.all()
    permission_classes = (IsAuthenticated,)



class RegionCreateAPIView(CreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionCreateSerializer
    permission_classes = (IsAuthenticated,)


class RegionUpdateAPIView(UpdateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (IsAuthenticated,)



class RegionDeleteAPIView(DestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (IsAuthenticated,)



class RegionListAPIView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        'name',
    ]
    ordering_fields = ['name']
    search_fields = ['name']




