from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import City,Region

User = get_user_model()

class CityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'name','region',
        ]




class CityListserializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'name','region',
        ]

class RegionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = [
            'name',
        ]

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['name']

