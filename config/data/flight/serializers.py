from rest_framework import serializers

from data.cars.models import Car  # Ensure you import the Car model
from employee.models import Employee
from employee.serializers import EmployeeListSerializer
from .models import Flight, Ordered
from ..cars.serializers import CarListserializer  # Import your CarListSerializer
from ..region.models import Region
from ..region.serializers import RegionSerializer
from ..upload.models import File
from ..upload.serializers import FileUploadSerializer

def clean_media_path(file_path):
    """
    Ensures the file path contains only a single occurrence of '/media'.
    """
    if file_path:
        return file_path.replace('/media/media/', '/media/')
    return file_path

class FlightListserializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(),allow_null=True)
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(),allow_null=True)  # Ensure this uses the Car model
    driver = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(),allow_null=True)
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
            "price",
            "price_type",

            "price_come_uzs",
            "price_come",
            "price_come_type",

            "driver_expenses",
            "driver_expenses_uzs",
            "driver_expenses_type",

            "flight_expenses",
            "flight_expenses_uzs",
            "flight_expenses_type",

            "other_expenses",
            "other_expenses_uzs",
            "other_expenses_type",

            "start_km",
            "end_km",
            "cargo_info",

            "flight_balance",
            "flight_balance_uzs",
            "flight_balance_type",

            "payment_type",

            "upload",
            "created_at",
            'is_archived',
        ]


    def to_representation(self, instance):
        """Customize the representation of fields."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        representation['region'] = RegionSerializer(instance.region).data
        if instance.upload:
            upload_data = FileUploadSerializer(instance.upload).data
            upload_data["file"] = clean_media_path(upload_data.get("file"))
            representation["upload"] = upload_data
        else:
            representation["upload"] = None

        return representation

    def update(self, instance, validated_data):
        # Update the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()  # Ensure save() is called to trigger signals
        return instance


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
            "price",
            "price_type",

            "driver_expenses",
            "driver_expenses_uzs",
            "driver_expenses_type",

            "flight_expenses",
            "flight_expenses_uzs",
            "flight_expenses_type",

            "other_expenses",
            "other_expenses_uzs",
            "other_expenses_type",

            "start_km",
            "end_km",
            "cargo_info",
            "flight_balance",
            "flight_balance_uzs",
            "flight_balance_type",
            "payment_type",
            "is_archived",

            "upload",
            "created_at",
        ]


    def to_representation(self, instance):
        """Customize the representation of fields."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        representation['region'] = RegionSerializer(instance.region).data
        representation['driver'] = EmployeeListSerializer(instance.driver).data
        if instance.upload:
            upload_data = FileUploadSerializer(instance.upload).data
            upload_data["file"] = clean_media_path(upload_data.get("file"))
            representation["upload"] = upload_data
        else:
            representation["upload"] = None

        return representation



class FlightOrderedListserializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Ordered
        fields = [
            "id",
            "region",
            "flight_type",
            "departure_date",

            "driver_expenses_uzs",
            "driver_expenses_type",
            "driver_expenses",

            "cargo_info",
            "driver_name",
            "driver_number",
            "car_number",
            "is_archived",

            "status",
            "created_at",
        ]

    def to_representation(self, instance):
        """Customize the representation of fields."""
        representation = super().to_representation(instance)
        representation['region'] = RegionSerializer(instance.region).data
        return representation