from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Oil, Remaining_oil_quantity, OilREcycles

User = get_user_model()




class OilCreateseralizer(serializers.ModelSerializer):
    class Meta:
        model = Oil
        fields = [
            "id",
            'oil_name',
            'oil_volume',
        ]


class Remaining_oil_quantityserializer(serializers.Serializer):
    class Meta:
        model = Remaining_oil_quantity
        fields = [
            "id",
            'oil_volume',
        ]


class RecycledOilSerializer(serializers.ModelSerializer):
    class Meta:
        model = OilREcycles
        fields = [
            "id",
            'oil',
            'amount',
            'car',
            'remaining_oil'
        ]
