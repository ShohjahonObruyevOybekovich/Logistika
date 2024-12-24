# from rest_framework import generics
from decimal import Decimal

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
from rest_framework.views import APIView

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




class BulkUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        updates = request.data  # Directly assign request.data as it is a list
        if not updates:
            return Response({"detail": "No updates provided"}, status=status.HTTP_400_BAD_REQUEST)

        updated_count = 0
        for update in updates:
            try:
                obj = Details.objects.get(id=update.get("id"))
                for field, value in update.items():
                    if field != "id":
                        if field == "car" and isinstance(value, str):  # Check if 'car' field is UUID
                            try:
                                car_instance = Car.objects.get(id=value)  # Convert UUID to Car instance
                                setattr(obj, field, car_instance)
                            except Car.DoesNotExist:
                                return Response({"detail": f"Car with id {value} not found."}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            setattr(obj, field, value)
                obj.save()
                updated_count += 1
            except Details.DoesNotExist:
                continue

        return Response({"detail": f"{updated_count} items updated successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        items_to_delete = request.data

        if not isinstance(items_to_delete, list) or not items_to_delete:
            return Response({"detail": "A list of items with IDs and prices is required"}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count = 0
        errors = []

        for item in items_to_delete:
            obj_id = item.get("id")
            price_uzs = Decimal(item.get("price_uzs", "0.00"))
            price_usd = Decimal(item.get("price_usd", "0.00"))

            try:
                obj = Details.objects.get(id=obj_id)
                Logs.objects.create(
                    action="INCOME",
                    amount_uzs=price_uzs,
                    amount_usd=price_usd,
                    kind="OTHER",
                    comment=f"Details sold for {price_usd} $",
                )
                obj.delete()
                deleted_count += 1
            except Details.DoesNotExist:
                errors.append({"id": obj_id, "detail": "Object not found"})
                continue

        response_data = {
            "detail": f"{deleted_count} items deleted successfully",
            "errors": errors
        }

        return Response(response_data, status=status.HTTP_200_OK)