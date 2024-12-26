from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from openpyxl.styles import Font, Alignment
from openpyxl.workbook import Workbook
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Salarka, Sale
from .serializers import (
    SalarkaCreateseralizer, SaleSerializer, SalarkaListSerializer
)


class SalarkaCreateAPIView(CreateAPIView):
    queryset = Salarka.objects.all()
    serializer_class = SalarkaCreateseralizer
    permission_classes = (IsAuthenticated,)


class SalarkaListAPIView(ListAPIView):
    queryset = Salarka.objects.all().order_by("-created_at")
    serializer_class = SalarkaListSerializer
    permission_classes = (IsAuthenticated,)


class SalarkaUpdateAPIView(UpdateAPIView):
    queryset = Salarka.objects.all()
    serializer_class = SalarkaCreateseralizer
    permission_classes = (IsAuthenticated,)


class SalarkaDeleteAPIView(DestroyAPIView):
    queryset = Salarka.objects.all()
    permission_classes = (IsAuthenticated,)


class SaleCreateAPIView(ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = (IsAuthenticated,)


class SaleRetrieveAPIView(RetrieveAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


import django_filters


class SalarkaFilter(django_filters.FilterSet):
    car_id = django_filters.UUIDFilter(field_name='car__id', lookup_expr='exact')

    class Meta:
        model = Salarka
        fields = ['car_id']


class SalarkaStatsAPIView(ListAPIView):
    serializer_class = SalarkaCreateseralizer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SalarkaFilter  # Use the filter class

    def get_queryset(self):
        # Retrieve the 'pk' (car_id) from the URL kwargs
        car_id = self.kwargs.get('pk')
        if car_id:
            # Filter the queryset by car_id
            return Salarka.objects.filter(car__id=car_id).order_by("-created_at")
        return Salarka.objects.none()



class FilteredSalarkaExportToExcelView(APIView):
    def get(self, request, *args, **kwargs):
        # Get filter parameters from query
        car_id = request.GET.get("car_id")  # Filter by car ID
        volume_filter = request.GET.get("volume")  # Filter by volume
        price_filter = request.GET.get("price_uzs")  # Filter by price_uzs

        # Start with the queryset for Salarka
        salarka_queryset = Salarka.objects.all()

        # Apply filters if parameters are provided
        if car_id:
            try:
                car_id = int(car_id)
                salarka_queryset = salarka_queryset.filter(car_id=car_id)
            except ValueError:
                return HttpResponse("Invalid car_id parameter.", status=400)

        if volume_filter:
            try:
                volume_filter = int(volume_filter)
                salarka_queryset = salarka_queryset.filter(volume=volume_filter)
            except ValueError:
                return HttpResponse("Invalid volume filter value.", status=400)

        if price_filter:
            try:
                price_filter = float(price_filter)
                salarka_queryset = salarka_queryset.filter(price_uzs=price_filter)
            except ValueError:
                return HttpResponse("Invalid price_uzs filter value.", status=400)

        # If no results, return a 404 error
        if not salarka_queryset.exists():
            return HttpResponse("No data found matching the filters.", status=404)

        # Create the Excel workbook
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Salarka Details"

        # Define headers
        headers = ["Car", "Volume", "Price (UZS)", "Created At", "Updated At"]
        sheet.append(headers)

        # Write the filtered data rows
        for salarka in salarka_queryset:
            sheet.append([
                salarka.car.name if salarka.car else "N/A",
                salarka.volume,
                salarka.price_uzs or "N/A",
                salarka.created_at.strftime('%Y-%m-%d %H:%M:%S') if salarka.created_at else "",
                salarka.updated_at.strftime('%Y-%m-%d %H:%M:%S') if salarka.updated_at else ""
            ])

        # Apply styles to the header row
        for col_num, header in enumerate(headers, 1):
            cell = sheet.cell(row=1, column=col_num)
            cell.font = Font(bold=True, size=12)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            sheet.column_dimensions[cell.column_letter].width = 20

        # Prepare the response to download the file
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="Salarka_Export.xlsx"'
        workbook.save(response)
        return response
