
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Salarka
from .serializers import (
    SalarkaCreateseralizer,
    SalarkaListserializer, SalarkaStatsSerializer
)


class SalarkaCreateAPIView(CreateAPIView):
    queryset = Salarka.objects.all()
    serializer_class = SalarkaCreateseralizer
    permission_classes = (IsAuthenticated,)


class SalarkaListAPIView(ListAPIView):
    queryset = Salarka.objects.all()
    serializer_class = SalarkaListserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]



class SalarkaUpdateAPIView(UpdateAPIView):
    queryset = Salarka.objects.all()
    serializer_class = SalarkaCreateseralizer
    permission_classes = (IsAuthenticated,)


class SalarkaDeleteAPIView(DestroyAPIView):
    queryset = Salarka.objects.all()
    permission_classes = (IsAuthenticated,)



# class Remaining_salarka_quantityListAPIView(ListAPIView):
#     queryset = Remaining_salarka_quantity.objects.all()
#     serializer_class = Remaining_salarka_quantityserializer
#     permission_classes = (IsAuthenticated,)
#     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
#     filterset_fields = ['purchased_volume
#     ']
#     ordering_fields = ['purchased_volume
#     ']
#     search_fields = ["purchased_volume
#     "]
#




class SalarkaStatsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        car_id = request.query_params.get("car_id")  # Get car ID from query params

        if not car_id:
            return Response(
                {"error": "car_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch all records for the given car ID
        salarka_data = Salarka.objects.filter(car_id=car_id)
        if not salarka_data.exists():
            return Response(
                {"message": "No data found for the specified car ID."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Calculate totals using the model's get_totals method
        totals = Salarka.get_totals(car_id)

        # Serialize the list of Salarka records
        serializer = SalarkaStatsSerializer(salarka_data, many=True)

        # Construct the response with detailed records and totals
        response_data = {
            "totals": totals,
            "details": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
