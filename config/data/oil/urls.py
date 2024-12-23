from django.urls import path


from data.oil.views import (
    OilCreateAPIView,
    OilUpdateAPIView,
    Remaining_oil_quantityListAPIView, RecycledOilAPIView, OilPurchaseAPIView, OilPurchaseUpdateAPIView,
    OilPurchaseListAPIView,
)

urlpatterns = [
    path("/<uuid:pk>",OilUpdateAPIView.as_view(), name="update"),
    path("list/",OilCreateAPIView.as_view(), name="list"),
    path('recycle/',RecycledOilAPIView.as_view(), name='recycle'),

    path('remaining-quantiry/',Remaining_oil_quantityListAPIView.as_view(), name='remaining-quantiry'),

    path("purchase/",OilPurchaseAPIView.as_view(), name="purchase"),
    path("purchase/<uuid:pk>/",OilPurchaseUpdateAPIView.as_view(), name="purchase"),
    path('oil-purchases/<uuid:pk>/', OilPurchaseListAPIView.as_view(), name='oil-purchases-list'),

]