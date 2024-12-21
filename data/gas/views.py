
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
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
    GasAnotherStationCreateseralizer,GasPurchaseListseralizer, GasAnotherListserializer)
from .models import GasPurchase,Gas_another_station


class GasPurchaseCreateAPIView(CreateAPIView):
    queryset = GasPurchase.objects.all()
    serializer_class = GasPurchaseCreateseralizer
    permission_classes = (IsAuthenticated,)


class GasPurchaseListAPIView(ListAPIView):
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
# class GasInventoryListAPIView(ListAPIView):
#     queryset = GasStation.objects.all()
#     serializer_class = GasStationListserializer
#     permission_classes = (IsAuthenticated,)
#     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
#     filterset_fields = ['gas_volume','last_payment',]
#     ordering_fields = ['last_gas_volume']
#     search_fields = ['last_gas_volume','last_payment']


#
# class GasStationCreateAPIView(CreateAPIView):
#     queryset = GasStation.objects.all()
#     serializer_class = GasStationCreateserializer
#     permission_classes = (IsAuthenticated,)
#
# class GasStationUpdateAPIView(UpdateAPIView):
#     queryset = GasStation.objects.all()
#     serializer_class = GasStationCreateserializer
#     permission_classes = (IsAuthenticated,)
#
#
# class GasStationDeleteAPIView(DestroyAPIView):
#     queryset = GasStation.objects.all()
#     permission_classes = (IsAuthenticated,)



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
                # Retrieve totals for the given station by pk
                totals = GasPurchase.get_totals(pk)
                purchases = GasPurchase.objects.filter(station=pk)  # Filter by station, not by id
                serializer = GasPurchaseListseralizer(purchases, many=True)

                return Response({
                    "station_id": pk,
                    "message": "Gas volume and prices retrieved successfully.",
                    "total_volume": totals["total_volume"],
                    "total_price_uzs": totals["total_price_uzs"],
                    "total_price_usd": totals["total_price_usd"],
                    "purchases": serializer.data,
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "Station ID is required."}, status=status.HTTP_400_BAD_REQUEST)

