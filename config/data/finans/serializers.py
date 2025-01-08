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
            "amount",
            "amount_type",

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
            "amount",
            "amount_type",

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
    car_price = serializers.SerializerMethodField()

    total_leasing_paid = serializers.SerializerMethodField()
    total_car_prices = serializers.SerializerMethodField()
    leasing_balance = serializers.SerializerMethodField()
    flight_count = serializers.SerializerMethodField()
    active_flight_count = serializers.SerializerMethodField()

    class Meta:
        model = Logs
        fields = [
            "id",
            "action",
            "amount_uzs",
            "amount",
            "amount_type",
            "car",
            "employee",
            "flight",
            "reason",
            "kind",
            "comment",
            "created_at",
            "income_sum",
            "outcome_sum",
            "car_price",
            "total_leasing_paid",
            "total_car_prices",
            "leasing_balance",
            "flight_count",
            "active_flight_count",
        ]

    def get_income_sum(self, obj):
        queryset = self.context.get('filtered_queryset', Logs.objects.all())
        return queryset.filter(action="INCOME").aggregate(total_income=Sum('amount_uzs'))['total_income'] or 0

    def get_outcome_sum(self, obj):
        queryset = (
            self.context.get('filtered_queryset', Logs.objects.all())
            .exclude(kind__iexact="BUY_CAR")
            .exclude(kind__isnull=True)
            .exclude(kind="")
        )

        return queryset.filter(action="OUTCOME").aggregate(total_outcome=Sum('amount_uzs'))['total_outcome'] or 0

    def get_car_price(self, obj):
        queryset = self.context.get('filtered_queryset', Logs.objects.filter(kind="BUY_CAR"))
        return queryset.filter(action="OUTCOME").aggregate(car_price=Sum('amount_uzs'))['car_price'] or 0

    def get_total_leasing_paid(self, obj):
        """
        Calculate the total amount paid for leasing based on Logs.
        """
        leasing_logs = Logs.objects.filter(kind="LEASING", action="OUTCOME").aggregate(
            total_leasing_paid=Sum('amount_uzs')
        )
        return leasing_logs['total_leasing_paid'] or 0

    def get_total_car_prices(self, obj):
        return Car.objects.filter(type_of_payment="LEASING").aggregate(
            total_car_prices=Sum('price_uzs')
        )['total_car_prices'] or 0

    def get_leasing_balance(self, obj):
        total_car_prices = self.get_total_car_prices(obj)
        total_leasing_paid = self.get_total_leasing_paid(obj)
        return total_car_prices - total_leasing_paid

    def get_flight_count(self, obj):
        # Get the date filter range from the context
        queryset = Flight.objects.all()
        start_date = self.context.get('start_date')
        end_date = self.context.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        return queryset.count()

    def get_active_flight_count(self, obj):
        # Filter active flights within the date range
        queryset = Flight.objects.filter(status="ACTIVE")
        start_date = self.context.get('start_date')
        end_date = self.context.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        return queryset.count()
