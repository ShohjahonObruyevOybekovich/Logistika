from django.urls import path


from data.oil.views import (
    OilCreateAPIView,
    OilUpdateAPIView,
    Remaining_oil_quantityListAPIView, RecycledOilAPIView, OilPurchasesListAPIView, OilPurchaseUpdateAPIView,
    UtilizedOilPurchaseListAPIView, UtilizedOilPurchaseUpdateAPIView, OilPurchaseListView, OilListAPIView,
)

urlpatterns = [
    path("/<uuid:pk>",OilUpdateAPIView.as_view(), name="update"),
    path("list/",OilCreateAPIView.as_view(), name="list"),
    path('recycle/',RecycledOilAPIView.as_view(), name='recycle'),
    path('list-pg/',OilListAPIView.as_view(), name='list-pg'),

    path('remaining-quantiry/',Remaining_oil_quantityListAPIView.as_view(), name='remaining-quantiry'),

    path("purchase/<uuid:pk>/",OilPurchasesListAPIView.as_view(), name="purchase"),
    path("purchase/<uuid:pk>/",OilPurchaseUpdateAPIView.as_view(), name="purchase"),
    path('oil-purchases/<uuid:pk>/', OilPurchaseListView.as_view(), name='oil-purchases-list'),

    # path("utilized/",UtilizedCreateApiView.as_view(), name="utilized"),
    path("utilized-create/",UtilizedOilPurchaseListAPIView.as_view(), name="utilized"),
    path("utilized/<uuid:pk>/",UtilizedOilPurchaseUpdateAPIView.as_view(), name="utilized"),

]