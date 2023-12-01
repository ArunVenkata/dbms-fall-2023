# coding=utf-8

from django.urls import re_path as path

from shop.views.product import ProductModelViewset
from shop.views.region import ChangeRegionView, RegionModelViewSet
from shop.views.transact import TransactView, TransactionHistory
from shop.models import *
from shop.views.store import StoreModelViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r"product", ProductModelViewset, basename="product")
router.register(r"store", StoreModelViewSet, basename="store")
router.register(r"region", RegionModelViewSet, basename="store")

urlpatterns = [
    path("transact/", TransactView.as_view(), name="transact-view"),
    path('change-region/', ChangeRegionView.as_view(), name="change-region"),
    path("transaction-history/", TransactionHistory.as_view(), name="transaction-history")
]

urlpatterns += router.urls
