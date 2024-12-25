from rest_framework import serializers

from data.cars.models import Car  # Ensure you import the Car model
from employee.models import Employee
from employee.serializers import EmployeeListserializer
from .models import Flight
from ..cars.serializers import CarListserializer  # Import your CarListSerializer
from ..region.models import Region
from ..region.serializers import RegionSerializer
from ..upload.models import File
from ..upload.serializers import FileUploadSerializer


class FlightListserializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())  # Ensure this uses the Car model
    driver = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    upload = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), allow_null=True)

    class Meta:
        model = Flight
        fields = [
            "id",
            "region",
            "flight_type",
            "route",
            "car",
            "driver",
            "status",
            "departure_date",
            "arrival_date",
            "price_uzs",
            # "price_usd",
            "driver_expenses_uzs",
            # "driver_expenses_usd",
            "cargo_info",
            "upload",
        ]

    def to_representation(self, instance):
        """Customize the representation of fields."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        representation['region'] = RegionSerializer(instance.region).data
        representation['upload'] = FileUploadSerializer(instance.upload).data
        return representation


class FlightListCReateserializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())  # Ensure this uses the Car model
    driver = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    upload = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), allow_null=True)

    class Meta:
        model = Flight
        fields = [
            "id",
            "region",
            "flight_type",
            "route",
            "car",
            "driver",
            "status",
            "departure_date",
            "arrival_date",
            "price_uzs",
            # "price_usd",
            "driver_expenses_uzs",
            # "driver_expenses_usd",
            "cargo_info",
            "upload",
        ]

    def to_representation(self, instance):
        """Customize the representation of fields."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        representation['region'] = RegionSerializer(instance.region).data
        representation['upload'] = FileUploadSerializer(instance.upload).data
        representation['driver'] = EmployeeListserializer(instance.driver).data
        return representation
