from django.urls import path
from .views import *
urlpatterns = [
    path('employee-create/',EmployeeCreateAPIView.as_view(), name='employee-create'),
    path('employee-list/',EmployeeListAPIView.as_view(), name='employee-list'),
    path('employee-update/<int:pk>/', EmployeeUpdateAPIView.as_view(), name='employee-update'),
    path('employee-by-id/<int:id>/',EmployeeInfo.as_view(), name='employee-by-id'),
    path('emplyee-delete/<int:pk>/', EmployeeDeleteAPIView.as_view(), name='emplyee-delete'),
]