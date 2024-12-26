from django.db import models

from data.command.models import TimeStampModel


class Logs(TimeStampModel):
    action = models.CharField(
        choices=[
            ("INCOME", "INCOME"),
            ("OUTCOME", "OUTCOME"),
        ]
        , max_length=20,
        null=True,
        blank=True
    )
    amount_uzs = models.FloatField(null=True, blank=True)
    # amount_usd = models.FloatField(null=True,blank=True)

    car = models.ForeignKey("cars.Car", on_delete=models.SET_NULL, null=True, blank=True)

    employee = models.ForeignKey(
        "employee.Employee", on_delete=models.SET_NULL, null=True, blank=True
    )

    flight = models.ForeignKey(
        "flight.Flight", on_delete=models.SET_NULL, null=True, blank=True
    )

    kind = models.CharField(
        choices=[
            ("OTHER", "Boshqa"),
            ("FIX_CAR", "Avtomobil tuzatish"),
            ("PAY_SALARY", "Oylik berish"),
            ("FLIGHT", "FLIGHT"),
            ("LEASING","Leasing"),
        ],
        max_length=20,
        null=True,
        blank=True
    )

    reason = models.TextField(null=True, blank=True)

    comment = models.TextField(null=True, blank=True)

    @classmethod
    def create_income(self, amount: float, comment: str):
        Logs.objects.create(
            action="INCOME", amount=amount, kind="OTHER", comment=comment
        )

    @classmethod
    def create_outcome(self, amount: float, comment: str):
        Logs.objects.create(
            action="OUTCOME", amount=amount, kind="OTHER", comment=comment
        )

    def __str__(self):
        return f"{self.action} - {self.amount_uzs}"



from django.db.models import Sum, F, Case, When, FloatField
from django.db.models.functions import TruncDay, TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class FilteredIncomeOutcomeAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("year", openapi.IN_QUERY, description="Filter by year", type=openapi.TYPE_INTEGER),
            openapi.Parameter("month", openapi.IN_QUERY, description="Filter by month", type=openapi.TYPE_INTEGER),
            openapi.Parameter("day", openapi.IN_QUERY, description="Filter by day", type=openapi.TYPE_INTEGER),
            openapi.Parameter("start_date", openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter("end_date", openapi.IN_QUERY, description="End date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter("action", openapi.IN_QUERY, description="Filter by action (INCOME, OUTCOME)", type=openapi.TYPE_STRING),
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
