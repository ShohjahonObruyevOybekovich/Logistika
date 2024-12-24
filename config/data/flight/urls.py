from django.urls import path
from .views import *

urlpatterns = [
    path("", FlightListAPIView.as_view(), name="flight-list"),
    # path("create/", FlightCreateAPIView.as_view(), name="flight-create"),
    path("<uuid:pk>/", FlightRetrieveAPIView.as_view(), name="flight-retrieve"),
               ]
