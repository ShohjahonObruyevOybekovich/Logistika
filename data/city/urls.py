from django.urls import path
from .views import *
urlpatterns = [
    path("create/",CityCreateAPIView.as_view(), name="create"),
    path("update/",CityUpdateAPIView.as_view(), name="update"),
    path("delete/",CityDeleteAPIView.as_view(), name="delete"),
    path("list/",CityListAPIView.as_view(), name="list"),

    path("region-create/",RegionCreateAPIView.as_view(), name="region-create"),
    path("region-update/",RegionUpdateAPIView.as_view(), name="region-update"),
    path("region-delete/",RegionDeleteAPIView.as_view(), name="region-delete"),
    path("region-list/",RegionListAPIView.as_view(), name="region-list"),
]