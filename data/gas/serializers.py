from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import GasPurchase, Gas_another_station

User = get_user_model()


# class GasStationListserializer(serializers.ModelSerializer):
#     class Meta:
#         model = GasStation
#         fields = [
#             "id",
#             'name',
#             'gas_volume',
#             'last_payment',
#
#         ]
# class GasStationCreateserializer(serializers.ModelSerializer):
#     class Meta:
#         model = GasStation
#         fields = [
#             "name",
#             "gas_volume",
#             "last_payment",
#         ]

class GasAnotherStationCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = Gas_another_station
        fields = [
            "car",
            'purchased_volume',
            'payed_price_uzs',
            'payed_price_usd'
        ]
class GasAnotherListserializer(serializers.ModelSerializer):
    class Meta:
        model = Gas_another_station
        fields = [
            'id',
            "car"
            'purchased_volume',
            'payed_price_uzs',
            'payed_price_usd'
        ]



class GasPurchaseCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = GasPurchase
        fields = [
            'purchased_volume',
            'payed_price_uzs',
            'payed_price_usd',
            'price_uzs',
            'price_usd',
            'station'
        ]
class GasPurchaseListseralizer(serializers.ModelSerializer):
    class Meta:
        model = GasPurchase
        fields = [
            'id',
            'purchased_volume',
            'payed_price_uzs',
            'payed_price_usd',
            'price_uzs',
            'price_usd',
            'station',
            'updated_at',
        ]
