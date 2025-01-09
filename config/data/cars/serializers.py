from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import serializers

from .models import Car, Model, Details, Notification
from ..finans.models import Logs

User = get_user_model()


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", 'name', 'number', 'model', 'type_of_payment',
            'leasing_period', 'with_trailer', 'fuel_type', "price",'price_uzs',"price_type",
            'distance_travelled', "oil_recycle_distance" ,"next_oil_recycle_distance",
                  "trailer_number","created_at", "updated_at"]


class CarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class CarListserializer(serializers.ModelSerializer):
    model = serializers.PrimaryKeyRelatedField(queryset=Model.objects.all())
    leasing_payed_amount = serializers.SerializerMethodField()
    monthly_payment = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            "id", "name", "number", "model", "type_of_payment",
            "leasing_period", "with_trailer", "fuel_type", "price",'price_uzs',"price_type",
            "distance_travelled", "oil_recycle_distance","next_oil_recycle_distance", "trailer_number",
            "leasing_payed_amount", "monthly_payment",
            "created_at", "updated_at"
        ]

    def get_leasing_payed_amount(self, instance):
        """
        Calculate the total amount paid for leasing based on Logs.
        """
        leasing_logs = Logs.objects.filter(car=instance, kind="LEASING", action="OUTCOME")
        total_payed = leasing_logs.aggregate(total=Sum('amount_uzs'))['total'] or 0
        return total_payed

    def get_monthly_payment(self, instance):
        """
        Calculate the monthly payment for leasing.
        """
        if instance.leasing_period and instance.price_uzs:
            return instance.price_uzs / instance.leasing_period
        return 0


    def to_representation(self, instance):
        res = super(CarListserializer, self).to_representation(instance)

        res['models'] = ModelSerializer(instance.model).data if instance.model else None

        return res


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'name']


class DetailCreateSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(),allow_null=True)

    class Meta:
        model = Details
        fields = [
            "id",
            "name",
            "id_detail",
            "car",
            "in_sklad",

            "price_uzs",
            "price",
            "price_type",

            "created_at",
            "updated_at",
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


class Notificationserializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id","message","is_read","created_at"]


