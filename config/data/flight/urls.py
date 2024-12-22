from django.urls import path
from .views import *

urlpatterns = [path("", FlightListAPIView.as_view())]
