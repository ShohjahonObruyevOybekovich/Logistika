from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Oil

User = get_user_model()


class OilListserializer(serializers.ModelSerializer):
    class Meta:
        model = Oil
        fields = [
            "id",
            'oil_name',
            'oil_volume',
            'paid_amount',
            'oil_price',
        ]

class OilCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = Oil
        fields = [
            'oil_name',
            'oil_volume',
            'paid_amount',
            'oil_price',
        ]

class Remaining_oil_quantityserializer(serializers.Serializer):
    class Meta:
        model = Oil
        fields = [
            'oil_volume'
        ]
