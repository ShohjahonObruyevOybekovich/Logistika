from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Oil, Remaining_oil_quantity

User = get_user_model()


class OilListserializer(serializers.ModelSerializer):
    class Meta:
        model = Oil
        fields = [
            "id",
            'oil_name',
            'oil_volume',
            'payed_price_uzs',
            'payed_price_usd',
            'price_uzs',
            'price_usd',
        ]

class OilCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = Oil
        fields = [
            'oil_name',
            'oil_volume',
            'payed_price_uzs',
            'payed_price_usd',
            'price_uzs',
            'price_usd',
        ]

class Remaining_oil_quantityserializer(serializers.Serializer):
    class Meta:
        model = Remaining_oil_quantity
        fields = [
            'oil_volume',
        ]

