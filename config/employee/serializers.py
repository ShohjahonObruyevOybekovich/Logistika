from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from data.upload.models import File
from data.upload.serializers import FileUploadSerializer
from .models import Employee

User = get_user_model()

def clean_media_path(file_path):
    """
    Ensures the file path contains only a single occurrence of '/media'.
    """
    if file_path:
        return file_path.replace('/media/media/', '/media/')
    return file_path


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "phone", "password", "can_delete")
        ref_name = "EmployeeUserCreateSerializer"

    def create(self, validated_data):
        # Ensure `can_delete` defaults to False if not explicitly provided
        can_delete = validated_data.get("can_delete", False)

        # Set superuser and staff status if `can_delete` is True
        is_superuser = is_staff = can_delete

        # Create the user instance
        user = User(
            full_name=validated_data["full_name"],
            phone=validated_data["phone"],
            can_delete=can_delete,
            is_superuser=is_superuser,
            is_staff=is_staff,
        )
        # Hash the password
        user.set_password(validated_data["password"])
        # Save the user instance
        user.save()

        return user





class EmployeeListSerializer(serializers.ModelSerializer):
    passport_photo = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), allow_null=True)
    license_photo = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), allow_null=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "full_name",
            "phone",
            "passport",
            "passport_photo",
            "license",
            "license_photo",
            "flight_type",
            "balance_uzs",
            "balance",
            "balance_price_type",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        ret = super(EmployeeListSerializer, self).to_representation(instance)
        if instance.passport_photo:
            photo_data = FileUploadSerializer(instance.passport_photo).data
            photo_data["file"] = clean_media_path(photo_data.get("file"))
            ret["passport_photo"] = photo_data
        else:
            ret["passport_photo"] = None

        if instance.license_photo:
            photo_data = FileUploadSerializer(instance.license_photo).data
            photo_data["file"] = clean_media_path(photo_data.get("file"))
            ret["license_photo"] = photo_data
        else:
            ret["license_photo"] = None

        return ret


class EmployeeCreateSerializer(serializers.ModelSerializer):
    passport_photo = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), allow_null=True)
    license_photo = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), allow_null=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "full_name",
            "phone",
            "passport",
            "passport_photo",
            "license",
            "license_photo",
            "flight_type",
            "balance_uzs",
            "balance",
            "balance_price_type",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        ret = super(EmployeeCreateSerializer, self).to_representation(instance)
        if instance.passport_photo:
            photo_data = FileUploadSerializer(instance.passport_photo).data
            photo_data["file"] = clean_media_path(photo_data.get("file"))
            ret["passport_photo"] = photo_data
        else:
            ret["passport_photo"] = None

        if instance.license_photo:
            photo_data = FileUploadSerializer(instance.license_photo).data
            photo_data["file"] = clean_media_path(photo_data.get("file"))
            ret["license_photo"] = photo_data
        else:
            ret["license_photo"] = None

        return ret
