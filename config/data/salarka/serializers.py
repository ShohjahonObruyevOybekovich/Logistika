from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.views import APIView

from .models import Salarka

User = get_user_model()


class SalarkaListserializer(serializers.ModelSerializer):
    class Meta:
        model = Salarka
        fields = [
            "id",
            'purchased_volume',
            'price_uzs',
            'price_usd'
        ]

class SalarkaCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = Salarka
        fields = [
            'purchased_volume',
            'price_usd',
            'price_uzs',
        ]
class SalarkaStatsSerializer(serializers.ModelSerializer):
    car_name = serializers.CharField(source="car.name", read_only=True)  # Add car name for readability

    class Meta:
        model = Salarka
        fields = [
            "id",
            "purchased_volume",
            "car_name",
            "price_uzs",
            "price_usd",
            "created_at",
            "updated_at",
        ]