from django.views import View
import openpyxl
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from openpyxl.styles import Font

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

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


class ExportLogsToExcelAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "action", openapi.IN_QUERY, description="Filter by action (INCOME, OUTCOME)", type=openapi.TYPE_STRING
            )
        ],
        responses={200: "Excel file generated"}
    )
    def get(self, request):
        action_filter = request.GET.get("action", None)
        if action_filter in ["INCOME", "OUTCOME"]:
            logs = Logs.objects.filter(action=action_filter).order_by("id")
        else:
            logs = Logs.objects.all().order_by("action", "id")

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Logs"
        headers = [
            "Action", "Miqdori (UZS)","Mashina", "Haydovchi" , "Reyis" ,
            "Turi", "Sababi", "Comment", "Yaratilgan vaqti"
                   ]
        for col_num, header in enumerate(headers, 1):
            cell = sheet.cell(row=1, column=col_num)
            cell.value = header

        for row_num, log in enumerate(logs, 2):
            sheet.cell(row=row_num, column=1).value = log.action
            sheet.cell(row=row_num, column=2).value = log.amount_uzs
            sheet.cell(row=row_num, column=3).value = log.car
            sheet.cell(row=row_num, column=4).value = log.employee.phone
            sheet.cell(row=row_num, column=5).value = log.flight.cargo_info
            sheet.cell(row=row_num, column=6).value = log.kind
            sheet.cell(row=row_num, column=7).value = log.reason
            sheet.cell(row=row_num, column=8).value = log.comment
            sheet.cell(row=row_num, column=9).value = log.created_at.strftime('%d-%m-%Y   %H:%M')

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="Logs_{action_filter or "All"}.xlsx"'
        workbook.save(response)
        return response