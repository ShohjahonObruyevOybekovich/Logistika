from django.contrib.auth import get_user_model
from rest_framework import serializers

from data.region.models import Region
from data.upload.serializers import FileUploadSerializer
from employee.models import Employee

from .models import Logs
from ..cars.models import Car
from ..cars.serializers import CarListserializer
from ..flight.models import Flight
from ..flight.serializers import FlightListserializer
from ..region.serializers import RegionSerializer

User = get_user_model()


class FinansListserializer(serializers.ModelSerializer):

    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(),allow_null=True)

    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all(),allow_null=True)

    driver = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(),allow_null=True)


    class Meta:
        model = Logs
        fields = [
            "id",
            "action",
            "amount_uzs",
            "amount_usd",
            "car",
            "driver",
            "flight",
            "kind",
            "comment",

        ]


    def to_representation_car(self, instance):
        """Customize the representation of the 'car' field."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        return representation

    def to_representation_driver(self, instance):
        """Customize the representation of the 'driver' field."""
        representation = super().to_representation(instance)
        representation['driver'] = RegionSerializer(instance.full_name).data
        return representation