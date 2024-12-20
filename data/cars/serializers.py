from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Car,Trailer_cars

User = get_user_model()

class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['driver', 'name','number','model_car','type_of_payment'
                  ,'lizing_period','with_trailer','fuel_type','car_price',
                  'distance_travelled']

        def validate_driver(self, value):
            if not User.objects.filter(pk=value.pk).exists():
                raise serializers.ValidationError("Driver does not exist.")
            return value


class CarListserializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id",'driver', 'name','number','model_car','type_of_payment'
                  ,'lizing_period','with_trailer','fuel_type','car_price',
                  'distance_travelled']




class TrailerCarsSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    class Meta:
        model = Trailer_cars
        fields = ['car','trailer_number']


class TrailerListSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    class Meta:
        model = Trailer_cars
        fields = ['car', 'number', 'model_car', 'number', 'trailer_number']

