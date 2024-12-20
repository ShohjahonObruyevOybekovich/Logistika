from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import GasPurchase, Gas_another_station,GasStation

User = get_user_model()


class GasStationListserializer(serializers.ModelSerializer):
    class Meta:
        model = GasStation
        fields = [
            "id",
            'name',
            'gas_volume',
            'last_payment',

        ]
class GasStationCreateserializer(serializers.ModelSerializer):
    class Meta:
        model = GasStation
        fields = [
            "name",
            "gas_volume",
            "last_payment",
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
            'station'
        ]
