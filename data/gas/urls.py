from django.urls import path
from .views import *
urlpatterns = [
    path("create/",GasPurchaseCreateAPIView.as_view(), name="create"),
    path("update/<uuid:id>",GasPurchaseUpdateAPIView.as_view(), name="update"),
    path("list/",GasPurchaseListAPIView.as_view(), name="list"),
    path('list-no-pg/',GasPurchasenopgListAPIView.as_view(), name="list-no-pg"),
    path('total/<uuid:pk>/', GasStationAPI.as_view(), name='gas_total'),


    #
    path("station-create/",GasStationCreateAPIView.as_view(), name="station-create"),
    path("station-list/",GasInventoryListAPIView.as_view(), name="station-list"),
    path("station-update/<uuid:pk>",GasStationUpdateAPIView.as_view(), name="station-update"),
    path("station-delete/<uuid:pk>",GasStationDeleteAPIView.as_view(), name="inventory-delete"),

    path('another-station-create/',GasAnotherStationCreateAPIView.as_view(), name='another-station-create'),
    path("another-station-update/<uuid:pk>",GasAnotherStationUpdateAPIView.as_view(), name="update"),
    path("another-station-delete/<uuid:pk>",GasAnotherStationDeleteAPIView.as_view(), name="delete"),
    path("another-station-list/",GasAnotherStationListAPIView.as_view(), name="list"),
    path('another-list-no-pg',GasAnotherStationnopgListAPIView.as_view(), name="list-no-pg"),
]
