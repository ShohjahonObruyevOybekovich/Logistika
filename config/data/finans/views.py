from django.shortcuts import render
from django.views import View
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from data.finans.models import Logs
from data.finans.serializers import FinansListserializer


class Finans(ListCreateAPIView):
    queryset = Logs
    serializer_class = FinansListserializer
    permission_classes = [IsAuthenticated]


class FinansDetail(RetrieveAPIView):
    queryset = Logs
    serializer_class = FinansListserializer
    permission_classes = [IsAuthenticated]

