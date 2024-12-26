from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Oil, Remaining_oil_quantity, OilREcycles, OilPurchase, Utilized_oil
from ..cars.models import Car
from ..cars.serializers import CarListserializer

User = get_user_model()


class OilCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = Oil
        fields = [
            "id",
            'oil_name',
            'oil_volume',
            "created_at",
            'updated_at',
        ]


class Remaining_oil_quantityserializer(serializers.Serializer):
    class Meta:
        model = Remaining_oil_quantity
        fields = [
            "id",
            'oil_volume',
            "updated_at",
        ]


class RecycledOilSerializer(serializers.ModelSerializer):
    oil = serializers.PrimaryKeyRelatedField(queryset=Oil.objects.all())
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    remaining_oil_quantity = serializers.SerializerMethodField()
    oil_recycle_distance = serializers.FloatField(write_only=True, required=False)
    next_oil_recycle_distance = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = OilREcycles
        fields = [
            "id",
            "oil",
            "amount",
            "car",
            "oil_recycle_distance",
            "next_oil_recycle_distance",
            "remaining_oil",
            "remaining_oil_quantity",
            "created_at",
        ]

    def get_remaining_oil_quantity(self, obj):
        """Get the remaining oil quantity."""
        remaining_oil = Remaining_oil_quantity.get()
        return remaining_oil.oil_volume

    def to_representation(self, instance):
        """Customize the representation of the 'car' field."""
        representation = super().to_representation(instance)
        representation["oil"] = OilCreateseralizer(instance.oil).data
        representation["car"] = CarListserializer(instance.car).data
        representation["oil_recycle_distance"] = instance.car.oil_recycle_distance
        representation["next_oil_recycle_distance"] = instance.car.next_oil_recycle_distance
        return representation

    def create(self, validated_data):
        """Handle creation of OilREcycles and update related Car fields."""
        # Extract custom fields for the Car model
        oil_recycle_distance = validated_data.pop("oil_recycle_distance", None)
        next_oil_recycle_distance = validated_data.pop("next_oil_recycle_distance", None)

        # Create the OilREcycles instance
        instance = super().create(validated_data)

        # Update the related Car model
        car = instance.car
        if oil_recycle_distance is not None:
            car.oil_recycle_distance = oil_recycle_distance
        car.save()

        return instance


class OilPurchaseSerializer(serializers.ModelSerializer):
    remaining_oil_quantity = serializers.SerializerMethodField()

    class Meta:
        model = OilPurchase
        fields = [
            "id",
            "oil",
            "price_uzs",
            # "price_usd",
            "amount_uzs",
            # "amount_usd",
            "oil_volume",
            "remaining_oil_quantity",
            "created_at",
        ]

    def get_remaining_oil_quantity(self, obj):
        remaining_oil = Remaining_oil_quantity.get()
        return remaining_oil.oil_volume


class Utilized_oilSerializer(serializers.ModelSerializer):
    remaining_oil_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Utilized_oil
        fields = [
            "id",
            "quantity_utilized",
            "price_uzs",
            # "price_usd",
            "remaining_oil_quantity",
            "created_at",
        ]

    def get_remaining_oil_quantity(self, obj):
        remaining_oil = Remaining_oil_quantity.get()
        return remaining_oil.oil_volume
