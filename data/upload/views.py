from django.shortcuts import render

from rest_framework.generics import CreateAPIView

from .serializers import FileUploadSerializer

# Create your views here.


class UploadFileAPIView(CreateAPIView):

    serializer_class = FileUploadSerializer
