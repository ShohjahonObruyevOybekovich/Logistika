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
            "flight_type",
            "flight_price",
            "flight_price_uzs",
            "flight_price_type",
            "driver_expenses",
            "driver_expenses_uzs",
            "driver_expenses_type",
        ]
