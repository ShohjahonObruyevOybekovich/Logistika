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
        # "amount_usd",
        "car",
        "employee",
        "flight",
        "reason",
        "kind",
        "comment",
        "created_at",
    ]
    ordering_fields = ["action","created_at"]
    search_fields = ["action", "reason","employee", "flight","created_at"]


class FinansDetail(RetrieveUpdateDestroyAPIView):
    queryset = Logs.objects.all()
    serializer_class = FinansListserializer
    permission_classes = [IsAuthenticated]


class FinansDriver(ListCreateAPIView):
    # queryset = Logs.objects.all()
    serializer_class = FinansListserializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        driver_id = self.kwargs.get('pk')
        if driver_id:
            return Logs.objects.filter(employee__id=driver_id, kind="PAY_SALARY")
        return Logs.objects.none()
