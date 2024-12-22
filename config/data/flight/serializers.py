from django.contrib.auth import get_user_model
from rest_framework import serializers

from data.region.models import Region
from data.upload.serializers import FileUploadSerializer
from employee.models import Employee

from .models import Flight

User = get_user_model()


class FlightListserializer(serializers.ModelSerializer):

    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())

    car = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())

    driver = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    upload = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())

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
            "created_at",
            "updated_at",
            "file",
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
