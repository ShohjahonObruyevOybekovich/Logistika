from rest_framework import serializers

from data.cars.models import Car
from data.cars.serializers import CarListserializer
from data.gas.models import GasPurchase, GasSale, GasStation
from data.gas.models import Gas_another_station


class GasStationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasStation
        fields = ["id", "name", "remaining_gas", "created_at", "updated_at"]

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
            "payed_price",
            "payed_price_type",

            "price_uzs",
            "price",
            "price_type",

            "created_at",
            "updated_at",
        ]


class GasSaleListSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    station = serializers.PrimaryKeyRelatedField(queryset=GasStation.objects.all())

    class Meta:
        model = GasSale
        fields = [
            "id",
            "station",
            "car",

            "payed_price_uzs",
            "payed_price",
            "payed_price_type",

            "price_uzs",
            "price",
            "price_type",

            "amount",

            "km",
            "km_car",

            "created_at",
        ]

    def to_representation(self, instance):
        """Customize the representation of the 'car' field."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        representation['station'] = GasStationListSerializer(instance.station).data  # Include station details
        return representation


class GasAnotherStationCreateseralizer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())

    class Meta:
        model = Gas_another_station
        fields = ["id", "car", "name", "purchased_volume",
                  "payed_price_uzs",
                  "payed_price",
                  "payed_price_type",
                  "km", "km_car",
                  "created_at",
                  ]

    def to_representation(self, instance):
        res = super().to_representation(instance)

        res['car'] = CarListserializer(instance.car).data

        return res


class GasAnotherListserializer(serializers.ModelSerializer):
    car = CarListserializer(read_only=True)

    class Meta:
        model = Gas_another_station
        fields = ["id", "car", "name", "purchased_volume",
                  "payed_price_uzs",
                  "payed_price",
                  "payed_price_type",
                  "created_at",
                  "km",
                  "km_car",
                  #                   "payed_price_usd"
                  ]
