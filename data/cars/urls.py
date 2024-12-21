from django.urls import path
from .views import *
urlpatterns = [
    path('create/', CarCreateAPIView.as_view(), name='create'),
    path('list/', CarsListAPIView.as_view(), name='list'),
    path('list-no-pg/',CarsList_no_pg_APIView.as_view(),name='list-no-pg'),
    path('by-id/<uuid:pk>/', CarByIDAPIView.as_view(), name='id'),
    path('update/<uuid:pk>/', CarUpdateAPIView.as_view(), name='update'),
]