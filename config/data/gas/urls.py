from django.urls import path
from .views import *


urlpatterns = [
    path("", GasStationListCreateAPIView.as_view(), name="list"),
    path("<uuid:pk>", RetrieveUpdateDestroyAPIView.as_view(), name="list"),
    path("<uuid:pk>/purchases", GasPurchasesListAPIView.as_view(), name="list"),
    path("<uuid:pk>/sales", GasSalesListAPIView.as_view(), name="list"),

    path("another-create",GasAnotherStationCreateAPIView.as_view(), name="create"),
    path("another-list",GasAnotherStationnopgListAPIView.as_view(), name="list"),
    path("another-update/<uuid:pk>",GasAnotherStationUpdateAPIView.as_view(), name="update"),
    path("another-delete/<uuid:pk>",GasAnotherStationDeleteAPIView.as_view(), name="delete"),
]
