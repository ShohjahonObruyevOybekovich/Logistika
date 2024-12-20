from django.urls import path
from .views import *
urlpatterns = [
    path("create/",CityCreateAPIView.as_view(), name="create"),
    path("update/<uuid:pk>",CityUpdateAPIView.as_view(), name="update"),
    path("delete/<uuid:pk>",CityDeleteAPIView.as_view(), name="delete"),
    path("list/",CityListAPIView.as_view(), name="list"),

    path("region-create/",RegionCreateAPIView.as_view(), name="region-create"),
    path("region-update/<uuid:pk>",RegionUpdateAPIView.as_view(), name="region-update"),
    path("region-delete/<uuid:pk>",RegionDeleteAPIView.as_view(), name="region-delete"),
    path("region-list/",RegionListAPIView.as_view(), name="region-list"),
]