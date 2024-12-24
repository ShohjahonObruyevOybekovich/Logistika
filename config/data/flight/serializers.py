from django.contrib.auth import get_user_model
from rest_framework import serializers

from data.region.models import Region
from data.upload.serializers import FileUploadSerializer
from employee.models import Employee

from .models import Flight
from ..cars.serializers import CarListserializer
from ..region.serializers import RegionSerializer

User = get_user_model()


class FlightListserializer(serializers.ModelSerializer):

    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())

    car = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())

    driver = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    upload = serializers.UUIDField()

    class Meta:
        model = Flight
        fields = [
            "id",
            "region",
            "flight_type",
            "car",
            "driver",
            "departure_date",
            "arrival_date",
            "price_uzs",
            "price_usd",
            "driver_expenses_uzs",
            "driver_expenses_usd",
            "cargo_info",
            "upload",
        ]

    def to_representation(self, instance):

        res = super().to_representation(instance)

        res["upload"] = (
            FileUploadSerializer(instance.upload, context=self.context).data
            if instance.upload
            else None
        )

    def to_representation_car(self, instance):
        """Customize the representation of the 'car' field."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        return representation
    def to_representation_region(self, instance):
        """Customize the representation of the 'region' field."""
        representation = super().to_representation(instance)
        representation['region'] = RegionSerializer(instance.name).data
        return representation

    def to_representation_driver(self, instance):
        """Customize the representation of the 'driver' field."""
        representation = super().to_representation(instance)
        representation['driver'] = RegionSerializer(instance.full_name).data
        return representation