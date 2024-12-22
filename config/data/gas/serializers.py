from rest_framework import serializers

from data.gas.models import GasPurchase, GasStation


class GasStationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = GasStation
        fields = ["id", "name", "remaining_gas"]


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

    def to_representation(self, instance: "GasPurchase"):

        res = super().to_representation(instance)

        res["station"] = GasStationListSerializer(instance.station).data

        return res
