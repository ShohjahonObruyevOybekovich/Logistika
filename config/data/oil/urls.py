from django.urls import path
from data.oil.views import (
    OilCreateAPIView,
    OilUpdateAPIView,
    OilListAPIView,
    OilDeleteAPIView,
    Remaining_oil_quantityListAPIView, RecycledOilAPIView,
)

urlpatterns = [
    path("create/",OilCreateAPIView.as_view(), name="create"),
    path("update/<uuid:pk>",OilUpdateAPIView.as_view(), name="update"),
    path("list/",OilListAPIView.as_view(), name="list"),
    path("delete/<uuid:pk>",OilDeleteAPIView.as_view(), name="delete"),
    path('recycle/',RecycledOilAPIView.as_view(), name='recycle'),

    path('remaining-quantiry/',Remaining_oil_quantityListAPIView.as_view(), name='remaining-quantiry'),
]