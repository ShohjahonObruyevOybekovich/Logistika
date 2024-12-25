from django.contrib.auth import get_user_model
from rest_framework import serializers

from employee.models import Employee
from .models import Logs
from ..cars.models import Car
from ..cars.serializers import CarListserializer
from ..flight.models import Flight
from ..region.serializers import RegionSerializer

User = get_user_model()


class FinansListserializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), allow_null=True)

    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all(), allow_null=True)

    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), allow_null=True)

    class Meta:
        model = Logs
        fields = [
            "id",
            "action",
            "amount_uzs",
            # "amount_usd",
            "car",
            "employee",
            "flight",
            "kind",
            "comment",

        ]

    def to_representation_car(self, instance):
        """Customize the representation of the 'car' field."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        return representation

    def to_representation_employee(self, instance):
        """Customize the representation of the 'employee' field."""
        representation = super().to_representation(instance)
        representation['employee'] = RegionSerializer(instance.full_name).data
        return representation
