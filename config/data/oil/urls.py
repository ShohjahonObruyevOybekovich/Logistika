from django.urls import path


from data.oil.views import (
    OilCreateAPIView,
    OilUpdateAPIView, OilPurchasesListAPIView, OilPurchaseUpdateAPIView,
    UtilizedOilPurchaseListAPIView, UtilizedOilPurchaseUpdateAPIView, OilListAPIView, OilDetailAPIView,
    RecycledOilListAPIView, RemainingOilPurchaseListAPIView, RecycledOilUpdateAPIView, RecycleListAPIView,
    OilDetailListAPIView, RecycleOilCARListAPIView, OilPurchaseReadAPIView, OilRecycleListsAPIView,
    ExportOilInfoAPIView,
)

urlpatterns = [
    path("/<uuid:pk>",OilUpdateAPIView.as_view(), name="update"),
    path("list/",OilCreateAPIView.as_view(), name="list"),


    path('recycle/', RecycledOilListAPIView.as_view(), name='recycled-oil-list'),
    path("recycle-list/", OilRecycleListsAPIView.as_view(), name="list"),
    path("recycle-car/",RecycleOilCARListAPIView.as_view(), name='recycled-oil-car'),
    path('recycle/<uuid:pk>/', RecycledOilUpdateAPIView.as_view(), name='recycled-oil-detail'),
    path('recycled/<uuid:pk>/',RecycleListAPIView.as_view(), name='recycled-oil-list'),
    path('list-pg/',OilListAPIView.as_view(), name='list-pg'),

    path('remaining/',RemainingOilPurchaseListAPIView.as_view(), name='remaining-quantiry'),

    path("purchase/<uuid:pk>/",OilPurchasesListAPIView.as_view(), name="purchase"),
    path("purchase-read/",OilPurchaseReadAPIView.as_view(), name="purchase-read"),
    path("purchase/<uuid:pk>/",OilPurchaseUpdateAPIView.as_view(), name="purchase"),

    path('oil-details/<uuid:pk>/', OilDetailListAPIView.as_view(), name='oil-details'),

    # path("utilized/",UtilizedCreateApiView.as_view(), name="utilized"),
    path("utilized-create/",UtilizedOilPurchaseListAPIView.as_view(), name="utilized"),
    path("utilized/<uuid:pk>/",UtilizedOilPurchaseUpdateAPIView.as_view(), name="utilized"),

    path("oil-info/", ExportOilInfoAPIView.as_view(), name="oil-info"),

]