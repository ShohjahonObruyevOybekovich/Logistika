from decimal import Decimal

import django_filters
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.openapi import Response
from drf_yasg.utils import swagger_auto_schema
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from data.flight.serializers import FlightListserializer, FlightListCReateserializer, FlightOrderedListserializer
from .models import Flight, Ordered
from ..finans.models import Logs
from ..finans.serializers import FinansListserializer


class FlightListAPIView(ListCreateAPIView):
    queryset = Flight.objects.all().order_by("-created_at")
    serializer_class = FlightListserializer
    # permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = [
        'flight_type', "route", "status"
    ]
    ordering_fields = ('flight_type', "route", "status")
    search_fields = ('flight_type', "route", "status")


class FlightRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all().order_by("-created_at")
    serializer_class = FlightListserializer
    permission_classes = [IsAuthenticated]


class FlightFilter(django_filters.FilterSet):
    car_id = django_filters.UUIDFilter(field_name='car__id', lookup_expr='exact')

    class Meta:
        model = Flight
        fields = ['car_id']


class FlightStatsAPIView(ListAPIView):
    serializer_class = FlightListCReateserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FlightFilter  # Use the filter class

    def get_queryset(self):
        car_id = self.kwargs.get('pk')
        if car_id:
            # Filter the queryset by car_id
            return Flight.objects.filter(car__id=car_id).order_by("-created_at")
        return Flight.objects.none()


class FlightHistoryAPIView(ListAPIView):
    serializer_class = FlightListCReateserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FlightFilter

    def get_queryset(self):
        driver_id = self.kwargs.get('pk')
        if driver_id:
            return Flight.objects.filter(driver__id=driver_id).order_by("-created_at")
        return Flight.objects.none()


class FlightHistoryStatsAPIView(ListAPIView):
    serializer_class = FlightListCReateserializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        flight_id = self.kwargs.get('pk')
        if flight_id:
            return Flight.objects.filter(id=flight_id).order_by("-created_at")
        return Flight.objects.none()

class FinanceFlightAPIView(ListAPIView):
    serializer_class = FinansListserializer

    def get_queryset(self):
        flight_id = self.kwargs.get('pk')
        if flight_id:
            return Logs.objects.filter(flight__id=flight_id).order_by("-created_at")
        return Logs.objects.none()

class FlightListNOPg(ListAPIView):
    serializer_class = FlightListCReateserializer
    permission_classes = (IsAuthenticated,)
    queryset = Flight.objects.all().order_by('-created_at')
    pagination_class = None  # Disable pagination for this view only

    def get_paginated_response(self, data):
        return Response(data)


class FlightOrderedListAPIView(ListCreateAPIView):
    serializer_class = FlightOrderedListserializer
    queryset = Ordered.objects.all().order_by("-created_at")
    permission_classes = (IsAuthenticated,)


class FlightOrderedRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Ordered.objects.all().order_by("-created_at")
    serializer_class = FlightOrderedListserializer
    permission_classes = (IsAuthenticated,)


class ExportFlightInfoAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("type", openapi.IN_QUERY, description="Type of data to export (flight, ordered)",
                              type=openapi.TYPE_STRING),
        ],
        responses={200: "Excel file generated"}
    )
    def get(self, request):
        data_type = request.GET.get("type", "flight")  # Default to flight if not specified

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Flight Info"

        # Handle different types of data
        if data_type == "flight":
            queryset = Flight.objects.all()
            headers = [
                "Регион", "Тип рейса", "Автомобиль", "Водитель",
                "Дата отправления", "Дата прибытия", "Цена (UZS)", "Расходы водителя (UZS)",
                "Информация о грузе", "Другие расходы", "Статус", "Дата создания"
            ]
            sheet.append(headers)

            for flight in queryset:
                sheet.append([
                    flight.region.name if flight.region else "",
                    "Рейсы внутри Узбекистана" if flight.flight_type == "In_uzb" else "Рейсы за пределы Узбекистана" if flight.flight_type else "",
                    flight.car.number if flight.car else "",
                    flight.driver.full_name if flight.driver else "",
                    flight.departure_date.strftime('%d-%m-%Y') if flight.departure_date else "",
                    flight.arrival_date.strftime('%d-%m-%Y') if flight.arrival_date else "",
                    flight.price_uzs or "",
                    flight.driver_expenses_uzs or "",
                    flight.cargo_info or "",
                    flight.other_expenses or "",
                    flight.get_status_display() if flight.status else "",
                    flight.created_at.strftime("%d-%m-%Y %H:%M") if flight.created_at else "",
                ])

        elif data_type == "ordered":
            queryset = Ordered.objects.all()
            headers = [
                "Имя водителя", "Номер водителя", "Номер автомобиля", "Информация о грузе",
                "Статус", "Дата отправления", "Цена (UZS)", "Расходы водителя (UZS)",
                "Регион", "Тип рейса", "Дата создания"
            ]
            sheet.append(headers)

            for ordered in queryset:
                sheet.append([
                    ordered.driver_name or "",
                    ordered.driver_number or "",
                    ordered.car_number or "",
                    ordered.cargo_info or "",
                    ordered.get_status_display() if ordered.status else "",
                    ordered.departure_date.strftime('%d-%m-%Y') if ordered.departure_date else "",
                    ordered.price_uzs or "",
                    ordered.driver_expenses_uzs or "",
                    ordered.region.name if ordered.region else "",
                    "Рейсы внутри Узбекистана" if ordered.flight_type == "In_uzb" else "Рейсы за пределы Узбекистана" if ordered.flight_type else "",
                    ordered.created_at.strftime('%d-%m-%Y %H:%M') if ordered.created_at else "",
                ])

        else:
            return HttpResponse("Invalid type parameter. Must be one of: flight, ordered.", status=400)

        # Apply styles to headers
        for col_num, header in enumerate(headers, 1):
            cell = sheet.cell(row=1, column=col_num)
            cell.font = Font(bold=True, size=12)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            sheet.column_dimensions[cell.column_letter].width = 20

        # Generate the response
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="Flight_Info_{data_type}.xlsx"'
        workbook.save(response)
        return response



from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from icecream import ic

class FlightCloseApi(APIView):
    def put(self, request, pk, *args, **kwargs):

        data = request.data
        try:
            flight = Flight.objects.get(id=pk)

            if flight.status == "INACTIVE":
                return Response({"detail": "Flight is already closed."}, status=status.HTTP_400_BAD_REQUEST)


            flight.status = "INACTIVE"

            # Parse arrival_date if provided
            arrival_date_str = data.get("arrival_date")
            if arrival_date_str:
                arrival_date = datetime.strptime(arrival_date_str, "%Y-%m-%d").date()
            else:
                arrival_date = flight.arrival_date

            # Update other fields
            flight.end_km = data.get("end_km", flight.end_km)
            flight.flight_balance = data.get("flight_balance", flight.flight_balance)
            flight.arrival_date = arrival_date

            # Save flight updates
            flight.save()


            ic("Updated flight details and saved.")

            # Calculate lunch payments safely
            lunch_payments = 0
            if flight.departure_date and flight.arrival_date:
                days = max((flight.arrival_date - flight.departure_date).days, 0)
                lunch_payments = flight.other_expenses_uzs * days

            flight.flight_balance_uzs = request.data.get("flight_balance_uzs", flight.flight_balance_uzs)
            if flight.flight_balance_uzs:
                try:
                    flight.flight_balance_uzs = float(flight.flight_balance_uzs)
                    flight.flight_expenses_uzs = flight.flight_balance_uzs
                except Exception as e:
                    return Response({"detail": f"Invalid data for flight_balance_uzs: {e}"},
                                    status=status.HTTP_400_BAD_REQUEST)
        # Update driver balance
            if flight.driver:
                print(f"Updating driver balance for {flight.driver.full_name}")
                driver = flight.driver

                driver.balance_uzs += float(flight.driver_expenses_uzs)
                driver.balance_uzs += float(lunch_payments)
                driver.balance_uzs -= float(flight.flight_balance_uzs)


                driver.save()


                flight.save()
                if flight.flight_balance_uzs > 0:
                    Logs.objects.create(
                        action="OUTCOME",
                        amount_uzs=flight.flight_balance_uzs,
                        kind="FLIGHT",
                        comment=f"{flight.driver.full_name} заплатил за рейс ${flight.flight_balance_uzs} ${flight.flight_balance_type}",
                        flight=flight,
                        employee=flight.driver
                        )
                Logs.objects.create(
                    action="OUTCOME",
                    amount_uzs=lunch_payments,
                    kind="FLIGHT",
                    comment=f"Расход на питание {lunch_payments} $",
                    flight=flight,
                    employee=flight.driver
                )
                Logs.objects.create(
                    action="OUTCOME",
                    amount_uzs=flight.flight_expenses_uzs,
                    kind="FLIGHT",
                    comment=f"{flight.driver.full_name} заплатил за рейс ${flight.flight_expenses_uzs} ${flight.flight_expenses_type}",
                    flight=flight,
                    employee=flight.driver
                )
                ic(f"Updated driver balance for {flight.driver.full_name}")
            else:
                print("Driver is None, skipping balance update")

            # Serialize and return response
            serializer = FlightListserializer(flight)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Flight.DoesNotExist:
            return Response({"detail": "Flight not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
