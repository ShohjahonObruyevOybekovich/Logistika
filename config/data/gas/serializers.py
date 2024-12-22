from rest_framework import serializers

from data.cars.models import Car
from data.gas.models import GasPurchase, GasSale, GasStation


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

    # def to_representation(self, instance: "GasPurchase"):

    #     res = super().to_representation(instance)

    #     res["station"] = GasStationListSerializer(instance.station).data

    #     return res


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
            "payed_price_uzs",
            "payed_price_usd",
            "price_uzs",
            "price_usd",
            "created_at",
        ]
