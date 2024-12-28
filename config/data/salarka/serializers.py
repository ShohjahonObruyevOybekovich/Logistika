from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Salarka, Sale, Remaining_volume
from ..cars.models import Car
from ..cars.serializers import CarListserializer

User = get_user_model()


class RemainingSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remaining_volume
        fields = [
            "id",
            "volume",
            "created_at",

        ]


class SalarkaListSerializer(serializers.ModelSerializer):
    remaining_volume = serializers.SerializerMethodField()

    class Meta:
        model = Salarka
        fields = [
            "id",
            "car",
            "volume",
            'price_uzs',
            "remaining_volume",
            "created_at",
        ]

    def get_remaining_volume(self, obj):
        """
        This method will be called for each Salarka instance.
        We query the Remaining_volume model based on custom logic.
        """
        # You can modify this query logic based on your requirements
        remaining_volume_instance = Remaining_volume.objects.first()

        if remaining_volume_instance:
            return RemainingSalesSerializer(remaining_volume_instance).data
        return None


    def to_representation(self, instance):
        """Customize the representation of the 'car' and 'remaining_volume' fields."""
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
            "price_uzs",
            "price",
            "price_type",
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
            "price",
            "price_type",
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
            "volume",
            "created_at",
        ]

    def to_representation(self, instance):
        """Customize the representation of the 'car' field."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        return representation


