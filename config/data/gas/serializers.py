from rest_framework import serializers

from data.cars.models import Car
from data.gas.models import GasPurchase, GasSale, GasStation

from data.gas.models import Gas_another_station


class GasStationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = GasStation
        fields = ["id", "name", "remaining_gas"]

        # make remaining_gas field read only
        read_only_fields = ["remaining_gas"]


class GasPurchaseListseralizer(serializers.ModelSerializer):

    station = GasStationListSerializer(read_only=True)

    class Meta:
        model = GasPurchase
        fields = [
            "id",
            "station",
            "amount",
            "payed_price_uzs",
            "payed_price_usd",
            "price_uzs",
            "price_usd",
            "created_at",
        ]


class GasSaleListseralizer(serializers.ModelSerializer):

    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())

    station = GasStationListSerializer(read_only=True)

    class Meta:
        model = GasSale
        fields = [
            "id",
            "station",
            "car",
            "amount",
            "created_at",
        ]


class GasAnotherStationCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = Gas_another_station
        fields = ["car", "purchased_volume", "payed_price_uzs", "payed_price_usd"]


class GasAnotherListserializer(serializers.ModelSerializer):
    class Meta:
        model = Gas_another_station
        fields = ["id", "car", "purchased_volume", "payed_price_uzs", "payed_price_usd"]
