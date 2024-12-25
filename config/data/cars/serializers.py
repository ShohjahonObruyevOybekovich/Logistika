from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Car, Model, Details

User = get_user_model()


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", 'name', 'number', 'model', 'type_of_payment'
            , 'leasing_period', 'with_trailer', 'fuel_type', 'price_uzs',
                                                             'distance_travelled', "trailer_number"]


class CarListserializer(serializers.ModelSerializer):
    model = serializers.PrimaryKeyRelatedField(queryset=Model.objects.all())

    class Meta:
        model = Car
        fields = ["id", 'name', 'number', 'model', 'type_of_payment'
            , 'leasing_period', 'with_trailer', 'fuel_type', "price_uzs",
                                                             'distance_travelled', "trailer_number"]

    def to_representation(self, instance):
        res = super(CarListserializer, self).to_representation(instance)

        res['models'] = ModelSerializer(instance.model).data if instance.model else None

        return res


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'name']


class DetailCreateSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())

    class Meta:
        model = Details
        fields = [
            "id",
            "name",
            "id_detail",
            "car",
            "price_uzs",
        ]

    def to_representation(self, instance):
        """Customize the representation of the 'car' field."""
        representation = super().to_representation(instance)
        representation['car'] = CarListserializer(instance.car).data
        return representation


class DetailCreateListSerializer(serializers.ListSerializer):
    child = DetailCreateSerializer()

    def create(self, validated_data):
        details = [Details(**data) for data in validated_data]
        return Details.objects.bulk_create(details)
