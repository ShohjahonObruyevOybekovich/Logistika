from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Flight,Route

User = get_user_model()


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class RouteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = 'start','end'



class FlightListserializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            "id",
            'region',
            'city',
            'route',
            'car',
            'driver',
            'departure_date',
            'arrival_date',
            'price_uzs',
            "price_usd",
            "driver_expenses_uzs",
            'driver_expenses_usd',
            'cargo_info',
            'uploaded_file',
            'status',
        ]

class FlightCreateserializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            "id",
            'region',
            'city',
            'route',
            'car',
            'driver',
            'departure_date',
            'arrival_date',
            'price_uzs',
            "price_usd",
            "driver_expenses_uzs",
            'driver_expenses_usd',
            'cargo_info',
            'uploaded_file',
            'status',
        ]

