from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Employee

User = get_user_model()


class EmployeeListserializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            'full_name',
            'phone',
            'passport',
            "passport_photo",
            'license',
            "license_photo",
            'flight_type',
            'balance_uzs',
            "balance",
            "balance_price_type",
            "created_at",
            "updated_at",
        ]


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            'full_name',
            'phone',
            'passport',
            "passport_photo",
            'license',
            "license_photo",
            'flight_type',
            'balance_uzs',
            "balance",
            "balance_price_type",
            "created_at",
            "updated_at",
        ]
