from django.contrib.admin.templatetags.admin_list import pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Oil, Remaining_oil_quantity, Recycled_oil
from .serializers import (
    OilCreateseralizer,
    OilListserializer,
    Remaining_oil_quantityserializer, RecycledOilSerializer
)


class OilCreateAPIView(CreateAPIView):
    queryset = Oil.objects.all()
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)


class OilListAPIView(ListAPIView):
    queryset = Oil.objects.all()
    serializer_class = OilListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['oil_name','oil_volume',]
    ordering_fields = ['oil_name']
    search_fields = ['oil_name','payed_price_uzs','payed_price_usd']


class OilUpdateAPIView(UpdateAPIView):
    queryset = Oil.objects.all()
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)


class OilDeleteAPIView(DestroyAPIView):
    queryset = Oil.objects.all()
    permission_classes = (IsAuthenticated,)



class Remaining_oil_quantityListAPIView(ListAPIView):
    queryset = Remaining_oil_quantity.objects.all()
    serializer_class = Remaining_oil_quantityserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['oil_volume']
    ordering_fields = ['oil_volume']
    search_fields = ["oil_volume"]


class RecycledOilAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # Fetch all recycled oil records
        oil_data = Recycled_oil.objects.all().order_by('-created_at')

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Optional: Override default page size
        paginated_data = paginator.paginate_queryset(oil_data, request)

        # Serialize the paginated data
        serializer = RecycledOilSerializer(paginated_data, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        # Process utilization of oil
        serializer = RecycledOilSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Recycled oil processed successfully.",
                             "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

