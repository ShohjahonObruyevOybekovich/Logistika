from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from data.finans.models import Logs
from data.finans.serializers import FinansListserializer


class Finans(ListCreateAPIView):
    queryset = Logs.objects.all()
    serializer_class = FinansListserializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        "action",
        "amount_uzs",
        "amount_usd",
        "car",
        "employee",
        "flight",
        "kind",
        "comment",
    ]
    ordering_fields = ["action"]
    search_fields = ["action","employee","flight"]


class FinansDetail(RetrieveUpdateDestroyAPIView):
    queryset = Logs.objects.all()
    serializer_class = FinansListserializer
    permission_classes = [IsAuthenticated]



