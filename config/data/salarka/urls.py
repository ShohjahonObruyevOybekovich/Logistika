from django.urls import path
from .views import *
urlpatterns = [
    path("create/",SalarkaCreateAPIView.as_view(), name="create"),
    path("update/<uuid:pk>",SalarkaUpdateAPIView.as_view(), name="update"),
    path("list/",SalarkaListAPIView.as_view(), name="list"),
    path("delete/<uuid:pk>",SalarkaDeleteAPIView.as_view(), name="delete"),

    path("salarka-total/<uuid:id>",SalarkaStatsAPIView.as_view(), name="salarka_total"),
    # path('remaining/',RemainingApiList.as_view(), name='remaining'),

    # path('remaining/',Remaining_salarka_quantityListAPIView.as_view(), name='remaining-salarka-list'),
]