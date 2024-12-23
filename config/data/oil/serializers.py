from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Oil, Remaining_oil_quantity, OilREcycles, OilPurchase, Utilized_oil

User = get_user_model()




class OilCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = Oil
        fields = [
            "id",
            'oil_name',
            'oil_volume',
        ]


class Remaining_oil_quantityserializer(serializers.Serializer):
    class Meta:
        model = Remaining_oil_quantity
        fields = [
            "id",
            'oil_volume',
        ]


class RecycledOilSerializer(serializers.ModelSerializer):
    class Meta:
        model = OilREcycles
        fields = [
            "id",
            'oil',
            'amount',
            'car',
            'remaining_oil'
        ]

    def get_remaining_oil_quantity(self, obj):
        remaining_oil = Remaining_oil_quantity.get()
        return remaining_oil.oil_volume



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

    class Meta:
        model = Utilized_oil
        fields = [
            "id",
            "quantity_utilized",
            "price_uzs",
            "price_usd",
        ]
    def get_remaining_oil_quantity(self, obj):
        remaining_oil = Remaining_oil_quantity.get()
        return remaining_oil.oil_volume

