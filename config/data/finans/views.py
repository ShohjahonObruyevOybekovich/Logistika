import openpyxl
from django.db.models import Sum, F, Case, When, FloatField
from django.db.models.functions import TruncDay, TruncMonth
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from data.finans.serializers import FinansListserializer, LogsFilter, FinansUserListserializer
from .models import Logs


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
    ordering_fields = ["action", "created_at"]
    search_fields = ["action", "reason", "employee", "flight", "created_at"]


class FinansList(ListAPIView):
    queryset = Logs.objects.all().order_by("-created_at")
    serializer_class = FinansUserListserializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = LogsFilter
    ordering_fields = ["action", "created_at"]
    search_fields = ["action", "reason", "employee", "flight", "created_at"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Extract date filters from query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Parse the dates if provided
        start_date = parse_datetime(start_date) if start_date else None
        end_date = parse_datetime(end_date) if end_date else None

        # Pass the filtered queryset and date range to the serializer context
        serializer = self.get_serializer(
            queryset,
            many=True,
            context={
                'filtered_queryset': queryset,
                'start_date': start_date,
                'end_date': end_date,
            }
        )

        # Paginate the results if necessary
        page = self.paginate_queryset(queryset)
        if page is not None:
            paginated_serializer = self.get_serializer(
                page,
                many=True,
                context={
                    'filtered_queryset': queryset,
                    'start_date': start_date,
                    'end_date': end_date,
                }
            )
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
            return Logs.objects.filter(employee__id=driver_id, kind="PAY_SALARY").order_by("created_at")
        return Logs.objects.none()

class FinansFlightExcel(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        # Fetch the data based on flight ID
        flight_id = pk
        logs = Logs.objects.filter(flight__id=flight_id, kind="FLIGHT").order_by("created_at")

        # Create an Excel workbook and sheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Flight Logs"

        # Define the headers in Russian
        headers = [
            "Название",        # Name
            "Сумма (UZS)",     # Amount (UZS)
            "Сумма (USD)",     # Amount (USD)
            "ID Рейса",        # Flight ID
            "Тип",             # Kind
            "Дата создания"    # Created At
        ]

        # Write the headers
        for col_num, header in enumerate(headers, start=1):
            col_letter = get_column_letter(col_num)
            ws[f"{col_letter}1"] = header

        # Write the data rows
        for row_num, log in enumerate(logs, start=2):
            ws[f"B{row_num}"] = log.name
            ws[f"C{row_num}"] = log.amount_uzs
            ws[f"D{row_num}"] = log.amount_usd
            ws[f"E{row_num}"] = log.flight.id if log.flight else None
            ws[f"F{row_num}"] = log.kind
            ws[f"G{row_num}"] = log.created_at.strftime('%d-%m-%Y %H:%M')

        # Set column widths for better readability
        for col_num, _ in enumerate(headers, start=1):
            ws.column_dimensions[get_column_letter(col_num)].width = 20

        # Save the workbook to an in-memory response
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f'attachment; filename="flight_logs_{flight_id}.xlsx"'
        wb.save(response)

        return response

class ExportLogsToExcelAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("action", openapi.IN_QUERY, description="Filter by action (INCOME, OUTCOME)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter("amount_uzs", openapi.IN_QUERY, description="Filter by amount in UZS",
                              type=openapi.TYPE_NUMBER),
            openapi.Parameter("car", openapi.IN_QUERY, description="Filter by car ID", type=openapi.TYPE_STRING),
            openapi.Parameter("employee", openapi.IN_QUERY, description="Filter by employee ID",
                              type=openapi.TYPE_STRING),
            openapi.Parameter("flight", openapi.IN_QUERY, description="Filter by flight ID", type=openapi.TYPE_STRING),
            openapi.Parameter("reason", openapi.IN_QUERY, description="Filter by reason", type=openapi.TYPE_STRING),
            openapi.Parameter("kind", openapi.IN_QUERY, description="Filter by kind", type=openapi.TYPE_STRING),
            openapi.Parameter("comment", openapi.IN_QUERY, description="Filter by comment", type=openapi.TYPE_STRING),
            openapi.Parameter("start_date", openapi.IN_QUERY, description="Filter by start date (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter("end_date", openapi.IN_QUERY, description="Filter by end date (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING),
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
        headers = ["Действие", "Сумма (UZS)", "Машина", "Водитель", "Рейс", "Тип", "Причина", "Комментарий",
                   "Время создания"]
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
            sheet.cell(row=row_num, column=9).value = log.created_at.strftime(
                '%d-%m-%Y   %H:%M') if log.created_at else ""

        # Response
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="Logs_{filters.get("action", "All")}.xlsx"'
        workbook.save(response)
        return response


class FilteredIncomeOutcomeAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("year", openapi.IN_QUERY, description="Filter by year", type=openapi.TYPE_INTEGER),
            openapi.Parameter("month", openapi.IN_QUERY, description="Filter by month", type=openapi.TYPE_INTEGER),
            openapi.Parameter("day", openapi.IN_QUERY, description="Filter by day", type=openapi.TYPE_INTEGER),
            openapi.Parameter("start_date", openapi.IN_QUERY, description="Start date (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter("end_date", openapi.IN_QUERY, description="End date (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter("action", openapi.IN_QUERY, description="Filter by action (INCOME, OUTCOME)",
                              type=openapi.TYPE_STRING),
        ],
        responses={200: "Filtered income and outcome sums with chart data"}
    )
    def get(self, request):
        # Extract query parameters
        year = request.GET.get("year")
        month = request.GET.get("month")
        day = request.GET.get("day")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        action = request.GET.get("action")  # Optional filter by action (INCOME, OUTCOME)

        # Base queryset
        queryset = Logs.objects.all()

        # Apply year, month, and day filters
        if year:
            queryset = queryset.filter(created_at__year=year)
            if month:
                queryset = queryset.filter(created_at__month=month)
                if day:
                    queryset = queryset.filter(created_at__day=day)

        # Apply custom date range filter
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            )

        # Apply action filter (optional)
        if action in ["INCOME", "OUTCOME"]:
            queryset = queryset.filter(action=action)

        # Calculate income and outcome sums
        income_sum = queryset.filter(action="INCOME").aggregate(total_income=Sum("amount_uzs"))["total_income"] or 0
        outcome_sum = queryset.filter(action="OUTCOME").aggregate(total_outcome=Sum("amount_uzs"))["total_outcome"] or 0

        # Determine grouping
        if start_date and end_date:
            group_by = TruncDay('created_at')
        elif year and month:
            group_by = TruncDay('created_at')
        elif year:
            group_by = TruncMonth('created_at')
        else:
            group_by = TruncMonth('created_at')

        # Generate chart data
        chart_data = (
            queryset
            .annotate(period=group_by)
            .values('period')
            .annotate(
                income=Sum(
                    Case(
                        When(action="INCOME", then=F('amount_uzs')),
                        default=0,
                        output_field=FloatField()
                    )
                ),
                outcome=Sum(
                    Case(
                        When(action="OUTCOME", then=F('amount_uzs')),
                        default=0,
                        output_field=FloatField()
                    )
                ),
            )
            .order_by('period')
        )

        # Prepare response data
        data = {
            "filters": {
                "year": year,
                "month": month,
                "day": day,
                "start_date": start_date,
                "end_date": end_date,
                "action": action,
            },
            "results": {
                "income_sum": income_sum,
                "outcome_sum": outcome_sum,
                "win": income_sum - outcome_sum,  # Net income
                "chart_data": list(chart_data)  # Grouped data for chart
            },
        }

        return Response(data)
