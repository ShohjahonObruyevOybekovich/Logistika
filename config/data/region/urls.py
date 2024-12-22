from django.urls import path
from .views import *

urlpatterns = [
    path("", RegionListAPIVIew.as_view()),
    path("<uuid:pk>", RegionDetailAPIView.as_view()),
]
