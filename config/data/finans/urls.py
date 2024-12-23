from django.urls import path
from .views import *

urlpatterns = [
    path("", Finans.as_view(), name="flight-list"),
    path("<uuid:pk>/", FinansDetail.as_view(), name="flight-retrieve"),
               ]
