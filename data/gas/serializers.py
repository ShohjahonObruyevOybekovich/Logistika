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
        ]
class GasStationCreateserializer(serializers.ModelSerializer):
    class Meta:
        model = GasStation
        fields = [
            'id',
            "name",
        ]

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
            "car",
            'purchased_volume',
            'payed_price_uzs',
            'payed_price_usd'
        ]



class GasPurchaseCreateseralizer(serializers.ModelSerializer):
    # station_uuid = serializers.UUIDField(source='station.id', read_only=True)  # Assuming 'station' has a UUID field

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
    station_name = serializers.CharField(source='station.name', read_only=True)
    class Meta:
        model = GasPurchase
        fields = [
            "id",
            'station_name',
            'purchased_volume',
            'payed_price_uzs',
            'payed_price_usd',
            'price_uzs',
            'price_usd',
            'station',
            'updated_at',
        ]
from django_filters import rest_framework as filters

class GasPurchaseFilter(filters.FilterSet):
    station_name = filters.CharFilter(field_name='station__name', lookup_expr='icontains')  # Filter by station name (case-insensitive)

    class Meta:
        model = GasPurchase
        fields = [
            'station',  # Filter by station ID
            'station_name',  # Filter by station name (via station relation)
            'purchased_volume',
            'payed_price_uzs',
            'payed_price_usd',
            'price_uzs',
            'price_usd',
        ]
