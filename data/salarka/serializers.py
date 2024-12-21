from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Salarka,Remaining_salarka_quantity

User = get_user_model()


class SalarkaListserializer(serializers.ModelSerializer):
    class Meta:
        model = Salarka
        fields = [
            "id",
            'oil_volume',
            'oil_price',
        ]

class SalarkaCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = Salarka
        fields = [
            'oil_volume',
            'oil_price',
        ]

class Remaining_salarka_quantityserializer(serializers.Serializer):
    class Meta:
        model = Remaining_salarka_quantity
        fields = [
            'oil_volume'
        ]
