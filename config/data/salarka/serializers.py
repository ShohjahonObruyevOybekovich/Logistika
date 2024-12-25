from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Salarka, Sale, Remaining_volume
from ..cars.models import Car
from ..cars.serializers import CarListserializer

User = get_user_model()


class SalarkaListSerializer(serializers.ModelSerializer):
    remaining_volume = serializers.SerializerMethodField()

    class Meta:
        model = Salarka
        fields = [
            "id",
            "car",
            "volume",
            # 'price_usd',
            'price_uzs',
            "remaining_volume",
        ]

    def get_remaining_volume(self, obj):
        # Get the current remaining volume
        remaining_volume = Remaining_volume.objects.first()
        return remaining_volume.volume if remaining_volume else 0

    def to_representation(self, instance):
        """Customize the representation of the 'car' field."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        return representation


class SalarkaCreateseralizer(serializers.ModelSerializer):
    # remaining_volume = Remaining_volume.objects.all()
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())

    class Meta:
        model = Salarka
        fields = [
            "id",
            "car",
            "volume",
            # 'price_usd',
            'price_uzs',
            "created_at",
        ]
        read_only_fields = ['created_at']

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
            # "price_usd",
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

    def to_representation(self, instance):
        """Customize the representation of the 'car' field."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        return representation


class RemainingSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remaining_volume
        fields = [
            "id",
            "volume",
        ]
