from django.contrib import admin
from django.http.request import HttpRequest
from userauth.models import User, SalesUser,BusinessUser, HomeUser
from django.db.models import Q
# Register your models here.
@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        q = super().get_queryset(request)
        # return q
        if request.user.is_staff and not request.user.is_superuser:
            return q.filter()
        return q
    def has_module_permission(self, request: HttpRequest) -> bool:
        res = super().has_module_permission(request)
        if not request.user.is_superuser:
            return False
        return res