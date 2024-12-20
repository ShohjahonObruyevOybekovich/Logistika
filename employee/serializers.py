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
            'city',
            'price_of_flight',""
            "departure_date",
            'cargo_description'
        ]

class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'full_name',
            'phone',
            'city',
            'price_of_flight',""
            "departure_date",
            'cargo_description'
        ]
