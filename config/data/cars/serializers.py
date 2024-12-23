from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Car
User = get_user_model()

class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [ 'name','number','model','type_of_payment'
                  ,'leasing_period','with_trailer','fuel_type','price_uzs',"price_usd",
                  'distance_travelled', "trailer_number"]



class CarListserializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", 'name','number','model','type_of_payment'
                  ,'leasing_period','with_trailer','fuel_type',"price_uzs","price_usd",
                  'distance_travelled',"trailer_number"]



class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", 'name']
        read_only_fields = ["id"]