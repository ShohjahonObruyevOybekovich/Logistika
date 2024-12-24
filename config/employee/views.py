# from rest_framework import generics
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, ListCreateAPIView
)
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from .models import Employee
User = get_user_model()

class EmployeeRetrieveAPIView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListserializer


class EmployeeCreateAPIView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateSerializer
    permission_classes = (IsAuthenticated,)



class EmployeeUpdateAPIView(UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateSerializer
    permission_classes = (IsAuthenticated,)

class EmployeeListAPIView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        'full_name',
            'phone',
            'passport',
            'license',
            'flight_type',
            'balance_uzs',
    ]
    ordering_fields = ['phone']
    search_fields = ['full_name',
            'phone',
            'passport',
            'license',
            'flight_type',
            'balance_uzs',]



class EmployeeDeleteAPIView(DestroyAPIView):
    queryset = Employee.objects.all()
    permission_classes = (IsAuthenticated,)

class EmployeeListCreateAPIView(ListAPIView):
    queryset = Employee.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EmployeeListserializer

    def get_paginated_response(self, data):
        return Response(data)

