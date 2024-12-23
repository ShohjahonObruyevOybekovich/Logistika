from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.views import APIView

from .models import Salarka, Sale
from ..cars.models import Car
from ..cars.serializers import CarListserializer

User = get_user_model()


class SalarkaListserializer(serializers.ModelSerializer):
    class Meta:
        model = Salarka
        fields = [
            "id",
            "car",
            "volume",
            'price_usd',
            'price_uzs',
        ]
    def to_representation(self, instance):
        """Customize the representation of the 'car' field."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        return representation

class SalarkaCreateseralizer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    class Meta:
        model = Salarka
        fields = [
            "id",
            "car",
            "volume",
            'price_usd',
            'price_uzs',
        ]

    def to_representation(self, instance):
        """Customize the representation of the 'car' field."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        return representation


class SalarkaStatsSerializer(serializers.ModelSerializer):
    car_name = serializers.CharField(source="car.name", read_only=True)  # Add car name for readability

    class Meta:
        model = Salarka
        fields = [
            "id",
            "car_name",
            "price_uzs",
            "price_usd",
            "created_at",
            "updated_at",
        ]

class SaleSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    class Meta:
        model = Sale
        fields = [
            "id",
            "car",
            "volume"
        ]