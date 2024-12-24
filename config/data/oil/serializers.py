from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
            'updated_at',
        ]


class Remaining_oil_quantityserializer(serializers.Serializer):
    class Meta:
        model = Remaining_oil_quantity
        fields = [
            "id",
            'oil_volume'
        ]


class RecycledOilSerializer(serializers.ModelSerializer):
    oil = serializers.PrimaryKeyRelatedField(queryset=Oil.objects.all())
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    remaining_oil_quantity = serializers.SerializerMethodField()
    class Meta:
        model = OilREcycles
        fields = [
            "id",
            "oil",
            'amount',
            'car',
            'remaining_oil',
            "remaining_oil_quantity",
        ]

    def get_remaining_oil_quantity(self, obj):
        remaining_oil = Remaining_oil_quantity.get()
        return remaining_oil.oil_volume

    def to_representation(self, instance):
        """Customize the representation of the 'car' field."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        return representation



class OilPurchaseSerializer(serializers.ModelSerializer):
    remaining_oil_quantity = serializers.SerializerMethodField()

    class Meta:
        model = OilPurchase
        fields = [
            "id",
            "oil",
            "price_uzs",
            "price_usd",
            "amount_uzs",
            "amount_usd",
            "oil_volume",
            "remaining_oil_quantity",
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
            "price_usd",
            "remaining_oil_quantity"
        ]

    def get_remaining_oil_quantity(self, obj):
        remaining_oil = Remaining_oil_quantity.get()
        return remaining_oil.oil_volume

