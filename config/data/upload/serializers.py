from root import settings
from root.settings import BASE_DIR, MEDIA_URL
from rest_framework import serializers

from .models import File


class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        file_url = instance.file.url  # Get the URL provided by the FileField

        # Ensure the URL is absolute
        request = self.context.get("request")  # Get the request from the context
        if request is not None:
            representation["file"] = request.build_absolute_uri(file_url)
        else:
            # Fallback to absolute URL using settings
            print(settings.MEDIA_URL, file_url.lstrip('/'))
            representation["file"] = f"{settings.MEDIA_URL}{file_url.lstrip('/')}"  # Avoid double slashes

        return representation

