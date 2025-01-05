# from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
)
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.serializers import UserCreateSerializer
from .models import Employee
from .serializers import *

User = get_user_model()


class EmployeeRetrieveAPIView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer


class EmployeeCreateAPIView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateSerializer
    permission_classes = (IsAuthenticated,)


class EmployeeUpdateAPIView(UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateSerializer
    permission_classes = (IsAuthenticated,)


class EmployeeListAPIView(ListAPIView):
    queryset = Employee.objects.all().order_by("-created_at")
    serializer_class = EmployeeListSerializer
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
                     'balance_uzs', ]


class EmployeeDeleteAPIView(DestroyAPIView):
    queryset = Employee.objects.all()
    permission_classes = (IsAuthenticated,)


class EmployeeListCreateAPIView(ListAPIView):
    queryset = Employee.objects.all().order_by("-created_at")
    permission_classes = (IsAuthenticated,)
    serializer_class = EmployeeListSerializer

    def get_paginated_response(self, data):
        return Response(data)



class RegisterADMINAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        # Validate incoming data using the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data
        full_name = serializer.validated_data.get('full_name')
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        # Check if the phone number already exists
        if User.objects.filter(phone=phone).exists():
            return Response({'success': False, 'message': 'This phone number is already registered.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Hash the password before creating the user
        user = User.objects.create(
            full_name=full_name,
            phone=phone,
        )
        user.set_password(password)  # Hash the password
        user.save()

        return Response({'success': True, 'message':  f"{full_name} user created successfully."}, status=status.HTTP_201_CREATED)
