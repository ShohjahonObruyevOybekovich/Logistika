from django.urls import path
from .views import *

urlpatterns = [
    path("", GasStationListCreateAPIView.as_view(), name="list"),
    path("<uuid:pk>", RetrieveUpdateDestroyAPIView.as_view(), name="list"),
]
