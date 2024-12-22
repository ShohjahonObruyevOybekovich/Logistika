from django.urls import path
from .views import *
urlpatterns = [
    path("create/",FlightCreateAPIView.as_view(), name="create"),
    path("update/<uuid:pk>",FlightUpdateAPIView.as_view(), name="update"),
    path("list/",FlightListAPIView.as_view(), name="list"),
    path("delete/<uuid:pk>",FlightDeleteAPIView.as_view(), name="delete"),

    # path('route-create/',RouteCreateAPIView.as_view(), name='route-create'),
    # path('route-update/<uuid:pk>',RouteUpdateAPIView.as_view(), name='route-update'),
    # path('route-list/',RouteListAPIView.as_view(), name='route-list'),
    # path('route-delete/<uuid:pk>',RouteDeleteAPIView.as_view(), name='route-delete'),

]