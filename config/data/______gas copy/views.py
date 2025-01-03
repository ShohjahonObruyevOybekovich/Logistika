
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
)
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (
    GasPurchaseCreateseralizer,
    GasAnotherStationCreateseralizer, GasAnotherListserializer, GasStationListserializer,
    GasStationCreateserializer, GasPurchaseFilter, GasPurchaseListseralizer)
from .models import GasPurchase, Gas_another_station, GasStation


class GasPurchaseCreateAPIView(CreateAPIView):
    queryset = GasPurchase.objects.all()
    serializer_class = GasPurchaseCreateseralizer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # Any custom logic when creating a GasPurchase, if needed
        serializer.save()

    def get_serializer_class(self):
        # Optionally override to handle different serializers
        return GasPurchaseCreateseralizer

class StationNameFilter(BaseFilterBackend):
    """
    Custom filter to allow filtering by station_name (derived field).
    """
    def filter_queryset(self, request, queryset, view):
        station_name = request.query_params.get('station_name')
        if station_name:
            queryset = queryset.filter(station__name__icontains=station_name)
        return queryset


class GasPurchaseListAPIView(ListAPIView):
    queryset = GasPurchase.objects.all()
    serializer_class = GasPurchaseListseralizer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = GasPurchaseFilter  # Use the custom filterset
    ordering_fields = ['purchased_volume']
    search_fields = [
        'purchased_volume',
        'payed_price_uzs',
        'payed_price_usd',
    ]




class GasPurchasenopgListAPIView(ListAPIView):
    queryset = GasPurchase.objects.all()
    serializer_class = GasPurchaseListseralizer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        'purchased_volume',
        'payed_price_uzs',
        'payed_price_usd',
        'price_uzs',
        'price_usd',
        "station",
    ]
    ordering_fields = ['purchased_volume']
    search_fields = ['purchased_volume',
                     'payed_price_uzs',
            'payed_price_usd'
                     ]
    def get_paginated_response(self, data):
        return Response(data)


class GasPurchaseUpdateAPIView(UpdateAPIView):
    queryset = GasPurchase.objects.all()
    serializer_class = GasPurchaseCreateseralizer
    permission_classes = (IsAuthenticated,)



#
class GasInventoryListAPIView(ListAPIView):
    queryset = GasStation.objects.all()
    serializer_class = GasStationListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['name',]
    ordering_fields = ['name']
    search_fields = ['name']

    def get_paginated_response(self, data):
        return Response(data)


class GasStationByIDAPIView(RetrieveAPIView):
    queryset = GasStation.objects.all()
    serializer_class = GasStationListserializer
    permission_classes = (IsAuthenticated,)


    def get_object(self):
        try:
            obj = self.get_queryset().get(pk=self.kwargs.get('pk'))  # Use 'pk' here
            self.check_object_permissions(self.request, obj)
            return obj
        except GasStation.DoesNotExist:
            raise NotFound("Car not found.")

class GasStationCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        name = request.data.get("name")  # Get the name from the request data
        if not name:
            return Response(
                {"error": "Name is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if a gas station with the same name exists
        existing_station = GasStation.objects.filter(name=name).first()
        if existing_station:
            # If the station exists, return its data
            response_serializer = GasStationCreateserializer(existing_station)
            return Response(
                {
                    "message": "A station with this name already exists.",
                    "existing_station": response_serializer.data,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # If no station with the same name exists, proceed with creation
        serializer = GasStationCreateserializer(data=request.data)
        if serializer.is_valid():
            gas_station = serializer.save()  # Save the new gas station
            response_serializer = GasStationCreateserializer(gas_station)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GasStationUpdateAPIView(UpdateAPIView):
    queryset = GasStation.objects.all()
    serializer_class = GasStationCreateserializer
    permission_classes = (IsAuthenticated,)


class GasStationDeleteAPIView(DestroyAPIView):
    queryset = GasStation.objects.all()
    permission_classes = (IsAuthenticated,)



class GasAnotherStationCreateAPIView(CreateAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherStationCreateseralizer
    permission_classes = (IsAuthenticated,)


class GasAnotherStationListAPIView(ListAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["car",'purchased_volume','payed_price_uzs',
            'payed_price_usd',]
    search_fields = ['purchased_volume','payed_price_uzs',
            'payed_price_usd']
    ordering_fields = ['purchased_volume']

class GasAnotherStationnopgListAPIView(ListAPIView):
    queryset = Gas_another_station.objects.all()
    serializer_class = GasAnotherListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['purchased_volume','payed_price_uzs',
            'payed_price_usd',]
    search_fields = ['purchased_volume','payed_price_uzs',
            'payed_price_usd']
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


from rest_framework.response import Response
from rest_framework import status
from .models import GasPurchase, GasStation
from .serializers import GasPurchaseListseralizer

class GasStationAPI(APIView):
    """
    API for managing and retrieving gas purchase data for a station.
    """

    def get(self, request, pk=None):
        """
        Retrieve the total gas volume and prices (UZS, USD) for a given station
        or details of a specific purchase by ID.
        """
        if pk:
            try:
                # Retrieve the station name for the given station ID (pk)
                station = GasStation.objects.filter(pk=pk).first()

                # If no station is found, return an error response
                if not station:
                    return Response({"error": "Station not found."}, status=status.HTTP_404_NOT_FOUND)

                # Retrieve totals for the given station by station ID
                totals = GasPurchase.get_totals(pk)

                # Filter purchases by station ID
                purchases = GasPurchase.objects.filter(station_id=pk)

                if purchases.exists():
                    # Serialize purchase details
                    serializer = GasPurchaseListseralizer(purchases, many=True)

                    return Response({
                        "station_name": station.name,  # Access the station name
                        "message": "Gas volume and prices retrieved successfully.",
                        "total_volume": totals["total_volume"],
                        "total_price_uzs": totals["total_price_uzs"],
                        "total_price_usd": totals["total_price_usd"],
                        "purchases": serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "station_name": station.name,  # Include station name even when no purchases found
                        "message": "No purchases found for the specified station."
                    }, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Station ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk=None):
        """
        Update a specific gas purchase record by ID.
        """
        if not pk:
            return Response({"error": "Station ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            purchase = GasPurchase.objects.get(id=pk)
        except GasPurchase.DoesNotExist:
            raise NotFound("Gas purchase not found.")

        # Use the serializer to validate and update the record
        serializer = GasPurchaseCreateseralizer(purchase, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Gas purchase updated successfully.",
                "purchase": serializer.data,
            }, status=status.HTTP_200_OK)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        """
        Partially update a specific gas purchase record by ID.
        """
        if not pk:
            return Response({"error": "Station ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            purchase = GasPurchase.objects.get(id=pk)
        except GasPurchase.DoesNotExist:
            raise NotFound("Gas purchase not found.")

        # Use the serializer to validate and partially update the record
        serializer = GasPurchaseCreateseralizer(purchase, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Gas purchase partially updated successfully.",
                "purchase": serializer.data,
            }, status=status.HTTP_200_OK)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Delete a specific gas purchase record by ID.
        """
        if not pk:
            return Response({"error": "Station ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            purchase = GasPurchase.objects.get(id=pk)
            purchase.delete()
            return Response({
                "message": "Gas purchase deleted successfully.",
            }, status=status.HTTP_204_NO_CONTENT)
        except GasPurchase.DoesNotExist:
            raise NotFound("Gas purchase not found.")