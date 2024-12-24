from django.urls import path
from .views import *


urlpatterns = [
    path("", EmployeeListAPIView.as_view(), name="employee-list"),
    path("<str:pk>", EmployeeRetrieveAPIView.as_view(), name="employee-detail"),
    path("list-pg",EmployeeListCreateAPIView.as_view(), name="employee-list-create"),
    path('create/',EmployeeCreateAPIView.as_view(), name='employee-create'),
    path('update/<str:pk>/', EmployeeUpdateAPIView.as_view(), name='employee-update'),
    path('delete/<str:pk>/', EmployeeDeleteAPIView.as_view(), name='emplyee-delete'),
]