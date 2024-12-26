from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView, get_object_or_404, CreateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Oil, Remaining_oil_quantity, OilREcycles, OilPurchase, Utilized_oil
from .serializers import (
    OilCreateseralizer,
    Remaining_oil_quantityserializer, RecycledOilSerializer, OilPurchaseSerializer, Utilized_oilSerializer
)


class OilCreateAPIView(ListCreateAPIView):
    queryset = Oil.objects.all().order_by("-created_at")
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)


class OilUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Oil.objects.all()
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)


class OilListAPIView(ListAPIView):
    queryset = Oil.objects.all().order_by("-created_at")
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)

    def get_paginated_response(self, data):
        return Response(data)


class RecycledOilListAPIView(CreateAPIView):
    queryset = OilREcycles.objects.all().order_by("-created_at")
    serializer_class = RecycledOilSerializer
    permission_classes = (IsAuthenticated,)



class RecycledOilUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OilREcycles.objects.all()
    serializer_class = RecycledOilSerializer
    permission_classes = (IsAuthenticated,)

class RecycleOilCARListAPIView(ListAPIView):
    serializer_class = RecycledOilSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Get the `car_id` from query parameters
        car_id = self.request.query_params.get("car_id")

        # Base queryset
        queryset = OilREcycles.objects.all().order_by("-created_at")

        # Filter by car_id if provided
        if car_id:
            queryset = queryset.filter(car__id=car_id)

        return queryset


class OilPurchasesListAPIView(CreateAPIView):
    serializer_class = OilPurchaseSerializer
    permission_classes = [IsAuthenticated]
    queryset = OilPurchase.objects.all().order_by("-created_at")

class OilPurchaseReadAPIView(ListAPIView):
    serializer_class = OilPurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the `car_id` from query parameters
        oil_id = self.request.query_params.get("oil_id")

        # Base queryset
        queryset = OilPurchase.objects.all().order_by("-created_at")

        if oil_id:
            queryset = queryset.filter(oil__id=oil_id)

        return queryset

class OilDetailAPIView(ListAPIView):
    """
    API view to fetch oil details including purchases, recycling, utilization history,
    and remaining oil quantity.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request,*args, **kwargs):
        oil = get_object_or_404(Oil, id=kwargs['pk'])
        utilizations = Utilized_oil.objects.all().order_by("-created_at")
        remaining_oil = Remaining_oil_quantity.objects.first()
        # Assuming you're fetching the first object

        data = {
            "oil_name": oil.oil_name,
            "oil_volume": oil.oil_volume,
            "remaining_oil_quantity": remaining_oil.oil_volume if remaining_oil else None,

            "utilizations": Utilized_oilSerializer(utilizations, many=True).data,
        }
        return Response(data)




class OilDetailListAPIView(ListAPIView):
    """
    API view to fetch oil details including purchases, recycling, utilization history,
    and remaining oil quantity.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        oil = get_object_or_404(Oil, id=kwargs['pk'])

        # Filter utilizations by oil ID
        utilizations = Utilized_oil.objects.all()  # Adjust 'oil' to match your field name

        # Fetch remaining oil quantity
        remaining_oil = Remaining_oil_quantity.objects.first()
        purchases = OilPurchase.objects.filter(oil=oil).order_by("-created_at")

        data = {
            "oil_name": oil.oil_name,
            "oil_volume": oil.oil_volume,
            "remaining_oil_quantity": remaining_oil.oil_volume if remaining_oil else None,
            "utilizations": Utilized_oilSerializer(utilizations, many=True).data,
            "purchases": OilPurchaseSerializer(purchases, many=True).data
        }
        return Response(data)


class OilRecycleListsAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = OilREcycles.objects.all().order_by("-created_at")
    serializer_class = RecycledOilSerializer


class RecycleListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]

    # serializer_class = RecycledOilSerializer
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        oil = get_object_or_404(Oil, id=pk)
        recycles = OilREcycles.objects.filter(oil=oil)
        data = {
            "oil_name": oil.oil_name,
            "recycles": [
                {
                    "id": recycle.id,
                    "amount": recycle.amount,
                    "car": recycle.car.name,
                    "remaining_oil": recycle.remaining_oil,
                    "updated_at": recycle.updated_at,
                }
                for recycle in recycles
            ],
        }
        return Response(data)


class OilPurchaseUpdateAPIView(RetrieveUpdateAPIView):
    queryset = OilPurchase.objects.all()
    serializer_class = OilPurchaseSerializer
    permission_classes = (IsAuthenticated,)




class UtilizedOilPurchaseListAPIView(ListCreateAPIView):
    queryset = Utilized_oil.objects.all().order_by("-created_at")
    serializer_class = Utilized_oilSerializer
    permission_classes = [IsAuthenticated]


class UtilizedOilPurchaseUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Utilized_oil.objects.all()
    serializer_class = Utilized_oilSerializer
    permission_classes = [IsAuthenticated]


class RemainingOilPurchaseListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # You can modify this method to filter or get data dynamically
        return Remaining_oil_quantity.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = Remaining_oil_quantityserializer(queryset, many=True)
        return Response(serializer.data)




from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Oil, OilPurchase, OilREcycles, Remaining_oil_quantity, Utilized_oil


class ExportOilInfoAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("type", openapi.IN_QUERY, description="Type of data to export (oil, purchase, recycle, utilized)", type=openapi.TYPE_STRING),
        ],
        responses={200: "Excel file generated"}
    )
    def get(self, request):
        data_type = request.GET.get("type", "oil")  # Default to oil if not specified

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Oil Info"

        # Handle different types of data
        if data_type == "oil":
            queryset = Oil.objects.all()
            headers = ["Название масла", "Объем масла (л)", "Дата создания", "Дата обновления"]
            sheet.append(headers)

            for oil in queryset:
                sheet.append([
                    oil.oil_name,
                    oil.oil_volume,
                    oil.created_at.strftime('%Y-%m-%d %H:%M:%S') if oil.created_at else "",
                    oil.updated_at.strftime('%Y-%m-%d %H:%M:%S') if oil.updated_at else ""
                ])

        elif data_type == "purchase":
            queryset = OilPurchase.objects.all()
            headers = ["Название масла", "Цена (UZS)", "Общая сумма (UZS)", "Объем масла (л)", "Дата создания", "Дата обновления"]
            sheet.append(headers)

            for purchase in queryset:
                sheet.append([
                    purchase.oil.oil_name if purchase.oil else "",
                    purchase.price_uzs,
                    purchase.amount_uzs,
                    purchase.oil_volume,
                    purchase.created_at.strftime('%Y-%m-%d %H:%M:%S') if purchase.created_at else "",
                    purchase.updated_at.strftime('%Y-%m-%d %H:%M:%S') if purchase.updated_at else ""
                ])

        elif data_type == "recycle":
            queryset = OilREcycles.objects.all()
            headers = ["Название масла", "Объем масла (л)", "Автомобиль", "Остаток масла (л)", "Дата создания", "Дата обновления"]
            sheet.append(headers)

            for recycle in queryset:
                sheet.append([
                    recycle.oil.oil_name if recycle.oil else "",
                    recycle.amount,
                    recycle.car.name if recycle.car else "",
                    recycle.remaining_oil,
                    recycle.created_at.strftime('%Y-%m-%d %H:%M:%S') if recycle.created_at else "",
                    recycle.updated_at.strftime('%Y-%m-%d %H:%M:%S') if recycle.updated_at else ""
                ])

        elif data_type == "utilized":
            queryset = Utilized_oil.objects.all()
            headers = ["Объем использованного масла (л)", "Цена (UZS)", "Дата создания", "Дата обновления"]
            sheet.append(headers)

            for utilized in queryset:
                sheet.append([
                    utilized.quantity_utilized,
                    utilized.price_uzs or "",
                    utilized.created_at.strftime('%Y-%m-%d %H:%M:%S') if utilized.created_at else "",
                    utilized.updated_at.strftime('%Y-%m-%d %H:%M:%S') if utilized.updated_at else ""
                ])

        else:
            return HttpResponse("Invalid type parameter. Must be one of: oil, purchase, recycle, utilized.", status=400)

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
        response["Content-Disposition"] = f'attachment; filename="Oil_Info_{data_type}.xlsx"'
        workbook.save(response)
        return response
