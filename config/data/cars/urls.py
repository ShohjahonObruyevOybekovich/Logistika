from django.urls import path
from .views import *
urlpatterns = [
    path('create/', CarCreateAPIView.as_view(), name='create'),
    path('list/', CarsListAPIView.as_view(), name='list'),
    path('list-no-pg/',CarsList_no_pg_APIView.as_view(),name='list-no-pg'),
    path('by-id/<uuid:pk>/', CarByIDAPIView.as_view(), name='id'),
    path('update/<uuid:pk>/', CarUpdateAPIView.as_view(), name='update'),

    path('delete/<uuid:uuid>',DeleteCarAPIView.as_view(), name='delete'),

    path('model-pagination/',ModelCarListAPIView.as_view(), name='model-list'),
    path('model/', ModelCarList_no_pg_APIView.as_view(), name='model-list'),
    path('model-create/', ModelCarCreateAPIView.as_view(), name='model'),
    path('model-update/<uuid:pk>', ModelCarUpdateAPIView.as_view(), name='model-update'),
    path('model-delete/<uuid:pk>', ModelCarDeleteAPIView.as_view(), name='model-delete'),

    path("bulk/", BulkCreateUpdateAPIView.as_view(), name="update"),
    path("detail/", DetailsView.as_view(), name="list"),
    path("detail-create/", DetailsCreateView.as_view(), name="create"),

]