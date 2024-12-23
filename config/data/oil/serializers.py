from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Oil, Remaining_oil_quantity, OilREcycles, OilPurchase, Utilized_oil

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
class OilPurchaseSerializer(serializers.ModelSerializer):
    oil  = serializers.PrimaryKeyRelatedField(queryset=Oil.objects.all())
    class Meta:
        model = OilPurchase
        fields = [
            "id",
            "oil",
            "price_uzs",
            "price_usd",
            "amount_uzs",
            "amount_usd",
            "oil_volume",
        ]

    def to_representation(self, instance):
        """Customize the representation of the 'oil' field."""
        representation = super().to_representation(instance)
        representation['oil'] = {
            "id": instance.oil.id,
            "oil_name": instance.oil.oil_name,
            "oil_volume": instance.oil.oil_volume
        }
        return representation


class Utilized_oilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilized_oil
        fields = [
            "id",
            "quantity_utilized",
            "price_uzs",
            "price_usd",
        ]

