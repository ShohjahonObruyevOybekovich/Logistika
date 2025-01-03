from root.settings import BASE_DIR
from rest_framework import serializers

from .models import File


class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")  # Get the request from the context
        if request is not None:
            representation["file"] = request.build_absolute_uri(instance.file.url)
        else:
            representation["file"] = f"{BASE_DIR}{instance.file.url}"
        return representation

