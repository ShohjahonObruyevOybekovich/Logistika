from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from openpyxl.styles import Font, Alignment
from openpyxl.workbook import Workbook
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, \
    DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from data.gas.models import GasPurchase, GasSale, GasStation
from data.gas.models import Gas_another_station
from data.gas.serializers import GasAnotherStationCreateseralizer, GasAnotherListserializer
from data.gas.serializers import (
    GasPurchaseListseralizer,
    GasSaleListSerializer,
    GasStationListSerializer, )
from root.pagination import GlobalPagination


class GasStationListCreateAPIView(ListCreateAPIView):
    serializer_class = GasStationListSerializer
    queryset = GasStation.objects.all().order_by("-created_at")
    pagination_class = GlobalPagination


class GasListAPIView(ListAPIView):
    serializer_class = GasStationListSerializer
    queryset = GasStation.objects.all().order_by("-created_at")

    def get_paginated_response(self, data):
        return Response(data)


class RetrieveUpdateDestroyerAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GasStationListSerializer
    queryset = GasStation.objects.all().order_by("-created_at")


class GasPurchasesListAPIView(ListCreateAPIView):
    serializer_class = GasPurchaseListseralizer

    def get_queryset(self):

        station = GasStation.objects.filter(pk=self.kwargs["pk"]).first()

        if not station:
            return GasPurchase.objects.none()

        return station.purchases.all().order_by("-created_at")

    def perform_create(self, serializer):

        station = GasStation.objects.filter(pk=self.kwargs["pk"]).first()

        if not station:
            raise NotFound("Gas station not found.")

        serializer.save(station=station)


class GasSalesListAPIView(ListCreateAPIView):
    serializer_class = GasSaleListSerializer

    def get_queryset(self):

        station = GasStation.objects.filter(pk=self.kwargs["pk"]).first()

        if not station:
            return GasSale.objects.none()

        return station.sales.all().order_by("-created_at")

    def perform_create(self, serializer):

        station = GasStation.objects.filter(pk=self.kwargs["pk"]).first()

        if not station:
            raise NotFound("Gas station not found.")

        serializer.save(station=station)


class GasAnotherStationCreateAPIView(ListCreateAPIView):
    queryset = Gas_another_station.objects.all().order_by("-created_at")
    serializer_class = GasAnotherStationCreateseralizer
    permission_classes = (IsAuthenticated,)


# class GasAnotherStationListAPIView(ListAPIView):
#     queryset = Gas_another_station.objects.all()
#     serializer_class = GasAnotherListserializer
#     permission_classes = (IsAuthenticated,)
#     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
#     filterset_fields = ["car",'purchased_volume','payed_price_uzs',
#             ]
#     search_fields = ['purchased_volume','payed_price_uzs',
#
#     ordering_fields = ['purchased_volume']

class GasAnotherStationnopgListAPIView(ListAPIView):
    queryset = Gas_another_station.objects.all().order_by("-created_at")
    serializer_class = GasAnotherListserializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['purchased_volume', 'payed_price_uzs',
                         ]
    search_fields = ['purchased_volume', 'payed_price_uzs',]

    ordering_fields = ['purchased_volume']

    def get_paginated_response(self, data):
        return Response(data)


class GasAnotherStationUpdateAPIView(UpdateAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherStationCreateseralizer
    permission_classes = (IsAuthenticated,)


class GasAnotherStationDeleteAPIView(DestroyAPIView):
    queryset = Gas_another_station.objects.all()
    permission_classes = (IsAuthenticated,)


class GasByCarID(ListAPIView):
    serializer_class = GasSaleListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        car_id = self.kwargs.get("pk")
        queryset = GasSale.objects.filter(car_id=car_id).order_by("-created_at")

        if not queryset.exists():
            raise NotFound("Gas Sale not found.")

        return queryset



class ExportGasInfoAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("type", openapi.IN_QUERY, description="Type of data to export (station, purchase, sale, another)", type=openapi.TYPE_STRING),
        ],
        responses={200: "Excel file generated"}
    )
    def get(self, request):
        data_type = request.GET.get("type", "station")  # Default to gas stations if not specified

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Gas Info"

        # Handle different types of data
        if data_type == "station":
            queryset = GasStation.objects.all()
            headers = ["Название", "Оставшийся газ", "Создано"]
            sheet.append(headers)

            for station in queryset:
                sheet.append([
                    station.name,
                    station.remaining_gas,
                    station.created_at.strftime('%d-%m-%Y %H:%M') if station.created_at else ""
                ])

        elif data_type == "purchase":
            queryset = GasPurchase.objects.all()
            headers = ["Станция", "Количество (м³)", "Оплаченная цена (UZS)", "Цена (UZS)", "Создано"]
            sheet.append(headers)

            for purchase in queryset:
                sheet.append([
                    purchase.station.name if purchase.station else "",
                    purchase.amount,
                    purchase.payed_price_uzs or "",
                    purchase.price_uzs or "",
                    purchase.created_at.strftime('%d-%m-%Y %H:%M') if purchase.created_at else ""
                ])

        elif data_type == "sale":
            queryset = GasSale.objects.all()
            headers = ["Станция", "Машина", "Количество (м³)", "Оплаченная цена (UZS)", "Цена (UZS)", "Создано"]

            sheet.append(headers)

            for sale in queryset:
                sheet.append([
                    sale.station.name if sale.station else "",
                    sale.car.name if sale.car else "",
                    sale.amount,
                    sale.payed_price_uzs or "",
                    sale.price_uzs or "",
                    sale.created_at.strftime('%d-%m-%Y %H:%M') if sale.created_at else "",
                ])

        elif data_type == "another":
            queryset = Gas_another_station.objects.all()
            headers = ["Машина", "Название станции", "Купленный объем (м³)", "Оплаченная цена (UZS)", "Создано"]
            sheet.append(headers)

            for another in queryset:
                sheet.append([
                    another.car.name if another.car else "",
                    another.name,
                    another.purchased_volume,
                    another.payed_price_uzs or "",
                    another.created_at.strftime('%d-%m-%Y %H:%M') if another.created_at else "",
                ])

        else:
            return HttpResponse("Invalid type parameter. Must be one of: station, purchase, sale, another.", status=400)

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
        response["Content-Disposition"] = f'attachment; filename="Gas_Info_{data_type}.xlsx"'
        workbook.save(response)
        return response
