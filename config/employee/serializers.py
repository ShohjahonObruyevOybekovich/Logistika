from django.contrib.auth import get_user_model
from rest_framework import serializers

from data.upload.models import File
from data.upload.serializers import FileUploadSerializer
from .models import Employee

User = get_user_model()


class EmployeeListserializer(serializers.ModelSerializer):
    passport_photo = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(),allow_null=True)
    license_photo = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(),allow_null=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            'full_name',
            'phone',
            'passport',
            "passport_photo",
            'license',
            "license_photo",
            'flight_type',
            'balance_uzs',
            "balance",
            "balance_price_type",
            "created_at",
            "updated_at",
        ]
    def to_representation(self, instance):
        ret = super(EmployeeListserializer, self).to_representation(instance)
        if instance.passport_photo:
            ret["passport_photo"] = FileUploadSerializer(instance.passport_photo).data
        else:
            ret["passport_photo"] = None

        if instance.license_photo:
            ret["license_photo"] = FileUploadSerializer(instance.license_photo).data
        else:
            ret["license_photo"] = None

        return ret


class EmployeeCreateSerializer(serializers.ModelSerializer):
    passport_photo = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(),allow_null=True)
    license_photo = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(),allow_null=True)
    class Meta:
        model = Employee
        fields = [
            "id",
            'full_name',
            'phone',
            'passport',
            "passport_photo",
            'license',
            "license_photo",
            'flight_type',
            'balance_uzs',
            "balance",
            "balance_price_type",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        ret = super(EmployeeCreateSerializer, self).to_representation(instance)
        if instance.passport_photo:
            ret["passport_photo"] = FileUploadSerializer(instance.passport_photo).data
        else:
            ret["passport_photo"] = None

        if instance.license_photo:
            ret["license_photo"] = FileUploadSerializer(instance.license_photo).data
        else:
            ret["license_photo"] = None

        return ret