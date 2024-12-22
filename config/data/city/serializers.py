from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import City, Region

User = get_user_model()


class RegionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Region
        fields = [
            "name",
            "price1",
            "price2",
        ]
