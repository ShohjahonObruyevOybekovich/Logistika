from django.urls import path

from .models import FilteredIncomeOutcomeAPIView
from .views import *

urlpatterns = [
    path("", Finans.as_view(), name="flight-list"),
    path("filter",FinansList.as_view(), name="flight-list"),
    path("<uuid:pk>/", FinansDetail.as_view(), name="flight-retrieve"),
    path("finans/driver/<int:pk>",FinansDriver.as_view(), name="flight-driver-detail"),

    path("export-logs/", ExportLogsToExcelAPIView.as_view(), name="export_logs"),

    path("info",FilteredIncomeOutcomeAPIView.as_view(), name="finans_info"),

               ]
