from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Flight,Route

User = get_user_model()


class GasStationListserializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = [
            "id",
            'name',
            'gas_volume',
            'last_payment',

        ]
class GasStationCreateserializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            "name",
            "gas_volume",
            "last_payment",
        ]

class GasAnotherStationCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            "id",
            'purchased_volume',
            'paid_amount'
        ]


class GasPurchaseCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            'id',
            'purchased_volume',
            'paid_amount',
            'gas_price',
            'station'
        ]
