from django.contrib.admin.templatetags.admin_list import pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView, get_object_or_404
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Oil, Remaining_oil_quantity, OilREcycles, OilPurchase
from .serializers import (
    OilCreateseralizer,
    Remaining_oil_quantityserializer, RecycledOilSerializer, OilPurchaseSerializer
)


class OilCreateAPIView(ListCreateAPIView):
    queryset = Oil.objects.all()
    serializer_class = OilCreateseralizer
    permission_classes = (IsAuthenticated,)


class OilUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Oil.objects.all()
    serializer_class = OilCreateseralizer
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
        oil_data = OilREcycles.objects.all().order_by('-created_at')

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


class OilPurchaseAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OilPurchaseSerializer
    queryset = OilPurchase.objects.all()


class OilPurchaseUpdateAPIView(RetrieveUpdateAPIView):
    queryset = OilPurchase.objects.all()
    serializer_class = OilPurchaseSerializer
    permission_classes = (IsAuthenticated,)


class OilPurchaseListAPIView(ListAPIView):
    """
    API view to list oil purchases filtered by oil UUID.
    """
    serializer_class = OilPurchaseSerializer
    permission_classes = [IsAuthenticated]  # Optional: Only allow authenticated users

    def get_queryset(self):
        oil_uuid = self.kwargs.get('pk')  # Get the oil UUID from the URL
        oil = get_object_or_404(Oil, id=oil_uuid)  # Validate that the oil exists
        return OilPurchase.objects.filter(oil=oil)  # Filter purchases by the oil

    def handle_exception(self, exc):
        if isinstance(exc, NotFound):
            return Response({'error': 'Oil not found'}, status=404)
        return super().handle_exception(exc)
