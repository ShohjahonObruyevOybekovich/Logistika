from django.urls import path
from .views import *
urlpatterns = [
    path("create/",GasPurchaseCreateAPIView.as_view(), name="create"),
    path("update/<uuid:id>",GasPurchaseUpdateAPIView.as_view(), name="update"),
    path("list/",GasPurchaseListAPIView.as_view(), name="list"),

    path("inventory-create/",GasInventoryListAPIView.as_view(), name="inventory-create"),
    path("inventory-update/",GasInventoryUpdateAPIView.as_view(), name="inventory-update"),
    path("inventory-delete/",GasInventoryDeleteAPIView.as_view(), name="inventory-delete"),

    path('another-station-create/',GasAnotherStationCreateAPIView.as_view(), name='another-station-create'),
    path("another-station-update/",GasAnotherStationUpdateAPIView.as_view(), name="update"),
    path("another-station-delete/",GasAnotherStationDeleteAPIView.as_view(), name="delete"),
    path("another-station-list/",GasAnotherStationListAPIView.as_view(), name="list"),
]