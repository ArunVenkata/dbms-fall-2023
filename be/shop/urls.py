# coding=utf-8

from django.urls import re_path as path

from shop.views.product import ProductModelViewset
from shop.views.region import ChangeRegionView, RegionModelViewSet
from shop.models import *
from shop.views.store import StoreModelViewSet

from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r"product", ProductModelViewset, basename="product")
router.register(r"store", StoreModelViewSet, basename="store")
router.register(r"region", RegionModelViewSet, basename="store")

urlpatterns = [
    # url(r'^$', views.index),
    # url(r'^add/$', views.add),
    # url(r'^edit/$', views.edit),
    # url(r'^delete/$', views.delete)
    # url('add', views.add),
    # url('edit', views.edit),
    path('change-region/', ChangeRegionView.as_view(), name="change-region")
    # url('delete', views.delete)
]
urlpatterns += router.urls
