from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Region

User = get_user_model()


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = [
            "id",
            "name",
            'route',
            "flight_type",
            "gone_flight_price",
            "gone_flight_price_uzs",
            "gone_flight_price_type",
            "gone_driver_expenses",
            "gone_driver_expenses_uzs",
            "gone_driver_expenses_type",
            "been_flight_price",
            "been_flight_price_uzs",
            "been_flight_price_type",
            "been_driver_expenses",
            "been_driver_expenses_uzs",
            "been_driver_expenses_type",
        ]
