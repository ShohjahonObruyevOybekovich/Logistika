# from rest_framework import generics
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView,
)
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .models import Car, Model
from ..finans.models import Logs


class CarCreateAPIView(CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarCreateSerializer
    # permission_classes = (IsAuthenticated,)


class CarsListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListserializer
    # permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        "name",
        "number",
        "type_of_payment",
        "with_trailer",
        "fuel_type",
        "price_uzs",
        "price_usd",
        "distance_travelled",
    ]
    ordering_fields = ["number"]
    search_fields = ["name"]


class CarsList_no_pg_APIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListserializer
    # permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        "name",
        "number",
        "type_of_payment",
        "with_trailer",
        "fuel_type",
        "price_uzs",
        "price_usd",
        "distance_travelled",
    ]
    ordering_fields = ["number"]
    search_fields = ["name"]

    def get_paginated_response(self, data):
        return Response(data)


class CarByIDAPIView(RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListserializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            obj = self.get_queryset().get(pk=self.kwargs.get("pk"))  # Use 'pk' here
            self.check_object_permissions(self.request, obj)
            return obj
        except Car.DoesNotExist:
            raise NotFound("Car not found.")


class CarUpdateAPIView(UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListserializer
    permission_classes = (IsAuthenticated,)


class ModelCarCreateAPIView(CreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = (IsAuthenticated,)

class ModelCarListAPIView(ListAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        'name'
    ]
    ordering_fields = ["name"]
    search_fields = ["name"]


class ModelCarList_no_pg_APIView(ListAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = (IsAuthenticated,)
    def get_paginated_response(self, data):
        return Response(data)

class ModelCarUpdateAPIView(UpdateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = (IsAuthenticated,)

class ModelCarDeleteAPIView(DestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = (IsAuthenticated,)


class DetailsCreateView(generics.ListCreateAPIView):
    queryset = Details.objects.all()
    serializer_class = DetailCreateListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # The serializer will automatically call create method of ListSerializer
        serializer.save()


class DetailsView(ListAPIView):
    queryset = Details.objects.all()
    serializer_class = DetailCreateSerializer
    permission_classes = [IsAuthenticated]


class DetailDeleteOrUpdateAPIView(GenericAPIView):
    """
    API view to delete a detail and add its price as income,
    or create/update records based on UUIDs.
    """
    queryset = Details.objects.all()
    serializer_class = DetailCreateListSerializer

    def delete(self, request, uuid,amount_uzs,amount_usd, *args, **kwargs):
        """
        Delete a detail by UUID and add its price to income.
        """
        detail = get_object_or_404(Details, uuid=uuid)

        # Add price to income
        Logs.objects.create(
            action="INCOME",
            amount_uzs=amount_uzs,
            amount_usd=amount_usd,

        )

        # Delete the detail
        detail.delete()
        return Response({"message": "Detail deleted and price added to income."}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        """
        Handle incoming data: Create or update details based on UUID.
        """
        incoming_data = request.data  # Expected to be a list of details
        results = {"created": 0, "updated": 0}

        for data in incoming_data:
            uuid = data.get("uuid")
            if not uuid:
                return Response({"error": "UUID is required for each detail."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if detail exists, update if yes, create if no
            detail, created = Details.objects.update_or_create(
                id=uuid,
                defaults={
                    "car": data.get("car"),
                    "name": data.get("name"),
                    "id_detail": data.get("id_detail"),
                    "price_uzs": data.get("price_uzs"),
                    "price_usd": data.get("price_usd"),
                },
            )

            if created:
                results["created"] += 1
            else:
                results["updated"] += 1

        return Response(
            {"message": "Details processed successfully.", "results": results},
            status=status.HTTP_200_OK,
        )

