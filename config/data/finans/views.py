from django.views import View
import openpyxl
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from openpyxl.styles import Font, Alignment

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from data.finans.models import Logs
from data.finans.serializers import FinansListserializer, LogsFilter, FinansUserListserializer


class Finans(ListCreateAPIView):
    queryset = Logs.objects.all().order_by("-created_at")
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



class FinansList(ListAPIView):
    queryset = Logs.objects.all().order_by("-created_at")
    serializer_class = FinansUserListserializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = LogsFilter  # Ensure this is set
    ordering_fields = ["action", "created_at"]
    search_fields = ["action", "reason", "employee", "flight", "created_at"]

    def list(self, request, *args, **kwargs):
        # Filter the queryset using LogsFilter
        queryset = self.filter_queryset(self.get_queryset())

        # Pass the filtered queryset to the serializer context
        serializer = self.get_serializer(queryset, many=True, context={'filtered_queryset': queryset})

        # Paginate the results if pagination is enabled
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_serializer = self.get_serializer(page, many=True, context={'filtered_queryset': queryset})
            return self.get_paginated_response(paginated_serializer.data)

        return Response(serializer.data)



class FinansDetail(RetrieveUpdateDestroyAPIView):
    queryset = Logs.objects.all().order_by("-created_at")
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



from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Logs
from django.db.models import Q


class ExportLogsToExcelAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("action", openapi.IN_QUERY, description="Filter by action (INCOME, OUTCOME)", type=openapi.TYPE_STRING),
            openapi.Parameter("amount_uzs", openapi.IN_QUERY, description="Filter by amount in UZS", type=openapi.TYPE_NUMBER),
            openapi.Parameter("car", openapi.IN_QUERY, description="Filter by car ID", type=openapi.TYPE_STRING),
            openapi.Parameter("employee", openapi.IN_QUERY, description="Filter by employee ID", type=openapi.TYPE_STRING),
            openapi.Parameter("flight", openapi.IN_QUERY, description="Filter by flight ID", type=openapi.TYPE_STRING),
            openapi.Parameter("reason", openapi.IN_QUERY, description="Filter by reason", type=openapi.TYPE_STRING),
            openapi.Parameter("kind", openapi.IN_QUERY, description="Filter by kind", type=openapi.TYPE_STRING),
            openapi.Parameter("comment", openapi.IN_QUERY, description="Filter by comment", type=openapi.TYPE_STRING),
            openapi.Parameter("start_date", openapi.IN_QUERY, description="Filter by start date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter("end_date", openapi.IN_QUERY, description="Filter by end date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        ],
        responses={200: "Excel file generated"}
    )
    def get(self, request):
        # Extract query parameters
        filters = {
            "action": request.GET.get("action"),
            "amount_uzs": request.GET.get("amount_uzs"),
            "car_id": request.GET.get("car"),
            "employee_id": request.GET.get("employee"),
            "flight_id": request.GET.get("flight"),
            "reason": request.GET.get("reason"),
            "kind": request.GET.get("kind"),
            "comment": request.GET.get("comment"),
        }
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        # Build the queryset with filters
        queryset = Logs.objects.all()

        # Apply field-specific filters
        for field, value in filters.items():
            if value:
                filter_kwargs = {field: value}
                queryset = queryset.filter(**filter_kwargs)

        # Apply date range filter
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            )

        # Generate Excel
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Logs"

        # Headers
        headers = ["Действие", "Сумма (UZS)", "Машина", "Водитель", "Рейс", "Тип", "Причина", "Комментарий", "Время создания"]
        for col_num, header in enumerate(headers, 1):
            cell = sheet.cell(row=1, column=col_num)
            cell.value = header
            cell.font = Font(bold=True, size=12)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            sheet.column_dimensions[cell.column_letter].width = 20

        # Rows
        for row_num, log in enumerate(queryset, 2):
            sheet.cell(row=row_num, column=1).value = log.action
            sheet.cell(row=row_num, column=2).value = log.amount_uzs
            sheet.cell(row=row_num, column=3).value = log.car.number if log.car else ""
            sheet.cell(row=row_num, column=4).value = log.employee.phone if log.employee else ""
            sheet.cell(row=row_num, column=5).value = log.flight.departure_date if log.flight else ""
            sheet.cell(row=row_num, column=6).value = log.kind if log.kind else ""
            sheet.cell(row=row_num, column=7).value = log.reason if log.reason else ""
            sheet.cell(row=row_num, column=8).value = log.comment if log.comment else ""
            sheet.cell(row=row_num, column=9).value = log.created_at.strftime('%d-%m-%Y   %H:%M') if log.created_at else ""

        # Response
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="Logs_{filters.get("action", "All")}.xlsx"'
        workbook.save(response)
        return response
