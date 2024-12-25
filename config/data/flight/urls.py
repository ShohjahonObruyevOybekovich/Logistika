from django.urls import path
from .views import *

urlpatterns = [
    path("", FlightListAPIView.as_view(), name="flight-list"),
    # path("create/", FlightCreateAPIView.as_view(), name="flight-create"),
    path("<uuid:pk>/", FlightRetrieveAPIView.as_view(), name="flight-retrieve"),
    path("stats/<uuid:pk>", FlightStatsAPIView.as_view(), name="flight-list"),
    path("driver/<int:pk>",FlightHistoryAPIView.as_view(), name="flight-history"),
    path("history/<uuid:pk>", FlightHistoryAPIView.as_view(), name="flight-history"),

    path("list-pg",FlightListNOPg.as_view(), name="flight-list-pg"),
               ]
