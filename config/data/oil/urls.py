from django.urls import path


from data.oil.views import (
    OilCreateAPIView,
    OilUpdateAPIView, OilPurchaseUpdateAPIView,
    UtilizedOilPurchaseListAPIView, UtilizedOilPurchaseUpdateAPIView, OilListAPIView, OilDetailAPIView,
    RecycledOilListAPIView, RemainingOilPurchaseListAPIView, RecycledOilUpdateAPIView, RecycleListAPIView,
)

urlpatterns = [
    path("/<uuid:pk>",OilUpdateAPIView.as_view(), name="update"),
    path("list/",OilCreateAPIView.as_view(), name="list"),


    path('recycle/', RecycledOilListAPIView.as_view(), name='recycled-oil-list'),
    path('recycle/<uuid:pk>/', RecycledOilUpdateAPIView.as_view(), name='recycled-oil-detail'),
    path('recycled/<uuid:pk>/',RecycleListAPIView.as_view(), name='recycled-oil-list'),
    path('list-pg/',OilListAPIView.as_view(), name='list-pg'),

    path('remaining/',RemainingOilPurchaseListAPIView.as_view(), name='remaining-quantiry'),

    path("purchase/<uuid:pk>/",OilDetailAPIView.as_view(), name="purchase"),
    path("purchase/<uuid:pk>/",OilPurchaseUpdateAPIView.as_view(), name="purchase"),
    # path('oil-details/<uuid:pk>/', OilDetailAPIView.as_view(), name='oil-details'),

    # path("utilized/",UtilizedCreateApiView.as_view(), name="utilized"),
    path("utilized-create/",UtilizedOilPurchaseListAPIView.as_view(), name="utilized"),
    path("utilized/<uuid:pk>/",UtilizedOilPurchaseUpdateAPIView.as_view(), name="utilized"),

]