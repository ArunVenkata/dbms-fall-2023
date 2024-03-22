from rest_framework.viewsets import ModelViewSet
from userauth.models import SalesUser
from userauth.enums import USER_TYPES
from shop.models.store import Store
from shop.serializers import StoreSerializer
from rest_framework.permissions import IsAuthenticated


class StoreModelViewSet(ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.user_type == USER_TYPES.salesperson:
            store_assigned = SalesUser.objects.filter(user_id=self.request.user.id).values_list("store_assigned_id", flat=True)[0]
            qs = qs.filter(id=store_assigned)
        elif self.request.user.user_type in [USER_TYPES.home, USER_TYPES.business]:
            qs = qs.filter(region_id=self.request.user.current_region_id)
        return qs
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context