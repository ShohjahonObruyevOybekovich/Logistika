from django.urls import path
from .views import *
urlpatterns = [
    path('car-create/', CarCreateAPIView.as_view(), name='create'),
    path('cars-list/', CarsListAPIView.as_view(), name='list'),
    path('cars-by-id/<uuid:pk>/', CarByIDAPIView.as_view(), name='id'),
    path('car-update/<uuid:pk>/', CarUpdateAPIView.as_view(), name='update'),
]