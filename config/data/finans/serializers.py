from django.contrib.auth import get_user_model
from django.db.models import Sum
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
            "reason",
            "kind",
            "comment",
            "created_at",

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



from django_filters import rest_framework as filters

class LogsFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    end_date = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Logs
        fields = [
            "action",
            "amount_uzs",
            "car",
            "employee",
            "flight",
            "reason",
            "kind",
            "comment",
            "created_at",
        ]



class FinansUserListserializer(serializers.ModelSerializer):
    income_sum = serializers.SerializerMethodField()
    outcome_sum = serializers.SerializerMethodField()
    win = serializers.SerializerMethodField()

    class Meta:
        model = Logs
        fields = [
            "id",
            "action",
            "amount_uzs",
            "car",
            "employee",
            "flight",
            "reason",
            "kind",
            "comment",
            "created_at",
            "income_sum",
            "outcome_sum",
            "win",
        ]

    def get_income_sum(self, obj):
        # Get the filtered queryset from the context
        queryset = self.context.get('filtered_queryset', Logs.objects.all())
        return queryset.filter(action="INCOME").aggregate(total_income=Sum('amount_uzs'))['total_income'] or 0

    def get_outcome_sum(self, obj):
        # Get the filtered queryset from the context
        queryset = self.context.get('filtered_queryset', Logs.objects.all())
        return queryset.filter(action="OUTCOME").aggregate(total_outcome=Sum('amount_uzs'))['total_outcome'] or 0

    def get_win(self, obj):
        # Calculate win as income - outcome
        income = self.get_income_sum(obj)
        outcome = self.get_outcome_sum(obj)
        return income - outcome
