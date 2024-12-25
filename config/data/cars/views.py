# from rest_framework import generics
from decimal import Decimal

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView, )
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Car, Model
from .serializers import *
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
        # "price_usd",
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
        # "price_usd",
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



class BulkCreateUpdateAPIView(APIView):
    """
    Handle bulk creation and updating of `Details` objects.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle both creation and updating of Details objects.
        """
        data = request.data  # Expecting a list of objects
        if not isinstance(data, list) or not data:
            return Response(
                {"detail": "A non-empty list of objects is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_count = 0
        updated_count = 0
        errors = []

        for item in data:
            obj_id = item.get("id")  # Extract ID if present
            car_id = item.get("car")  # Extract car ID if present
            try:
                if obj_id:  # Update logic
                    detail = Details.objects.get(id=obj_id)
                    for field, value in item.items():
                        if field == "car" and car_id:
                            try:
                                car_instance = Car.objects.get(id=car_id)
                                setattr(detail, field, car_instance)
                            except Car.DoesNotExist:
                                errors.append({"id": obj_id, "detail": f"Car with id {car_id} not found"})
                                continue
                        elif field != "id":
                            setattr(detail, field, value)
                    detail.save()
                    updated_count += 1
                else:  # Create logic
                    if car_id:  # Resolve car foreign key for new object
                        try:
                            item["car"] = Car.objects.get(id=car_id)
                        except Car.DoesNotExist:
                            errors.append({"detail": f"Car with id {car_id} not found"})
                            continue
                    Details.objects.create(**item)
                    created_count += 1
            except Details.DoesNotExist:
                errors.append({"id": obj_id, "detail": "Object not found for update"})
            except Exception as e:
                errors.append({"id": obj_id, "detail": str(e)})

        # Prepare the response
        response_data = {
            "created_count": created_count,
            "updated_count": updated_count,
            "errors": errors,
        }

        return Response(response_data, status=status.HTTP_200_OK)



class DeleteCarAPIView(APIView):
    """
    API endpoint to delete a car. Logs the car's sell price before deletion.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        Handle the deletion of a car and log the sell price.
        """
        car_id = kwargs.get('uuid')  # Car UUID from URL
        sell_price = request.data.get('sell_price')  # Sell price from request data

        if not sell_price:
            return Response(
                {"detail": "Sell price is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Convert sell price to Decimal
            sell_price_uzs = Decimal(sell_price)

            # Get the car by its UUID
            car = Car.objects.get(id=car_id)

            # Log the sell price in the Logs model
            Logs.objects.create(
                action="INCOME",
                amount_uzs=sell_price_uzs,
                car=car,
                kind="OTHER",
                comment=f"Car {car.name} - {car.number} sold for {sell_price_uzs} UZS."
            )

            # Delete the car
            car.delete()

            return Response(
                {"detail": f"Car {car.name} successfully deleted and sell price logged."},
                status=status.HTTP_200_OK
            )

        except Car.DoesNotExist:
            return Response(
                {"detail": "Car not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )