from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.db.models import Q

# Register your models here.

from shop.models import UserTransaction, Store, Product, Region


@admin.register(Region)
class RegionModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        q = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            return q.filter(manager_id=f"{request.user.id}")
        return q


@admin.register(Store)
class StoreModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        q = super().get_queryset(request)

        if request.user.is_staff and not request.user.is_superuser:
            return q.filter(manager_id=f"{request.user.id}")

        return q


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        q = super().get_queryset(request)
        return q
        return q


@admin.register(UserTransaction)
class UserTransactionModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        q = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            return q.filter(salesperson_id=f"{request.user.id}")
        return q


print("REGISTER ADMINS")
