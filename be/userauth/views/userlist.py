from rest_framework.viewsets import ModelViewSet
from userauth.enums import USER_TYPES
from userauth.models import User
from userauth.serializers import UserViewsetSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class UserModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserViewsetSerializer
    queryset = User.objects.all()
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        if self.request.user.user_type != USER_TYPES.salesperson:
            return qs.filter(Q(id=self.request.user.id) | Q(user_type=USER_TYPES.salesperson))
        return qs.filter(user_type=self.request.user.user_type)
