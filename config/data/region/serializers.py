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
            "price1",
            "price2",
        ]
