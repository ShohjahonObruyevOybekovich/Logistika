from django.urls import path
from .views import *

urlpatterns = [
    path("", FlightListAPIView.as_view(), name="flight-list"),
    path("<uuid:pk>/", FlightRetrieveAPIView.as_view(), name="flight-retrieve"),
               ]
