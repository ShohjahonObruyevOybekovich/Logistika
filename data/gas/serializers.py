from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import GasPurchase, GasInventory, Gas_another_station

User = get_user_model()


class GasInventoryListserializer(serializers.ModelSerializer):
    class Meta:
        model = GasInventory
        fields = [
            "id",
            'remaining_gas_volume',
            'remaining_payment',
        ]

class GasAnotherStationCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = Gas_another_station
        fields = [
            "id",
            'purchased_volume',
            'paid_amount'
        ]


class GasPurchaseCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = GasPurchase
        fields = [
            'id',
            'purchased_volume',
            'paid_amount',
            'gas_price',
            'station_name'
        ]
