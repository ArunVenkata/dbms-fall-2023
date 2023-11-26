from rest_framework.viewsets import ModelViewSet
from userauth.models import User
from userauth.serializers import UserViewsetSerializer



class UserModelViewSet(ModelViewSet):
    serializer_class = UserViewsetSerializer
    queryset = User.objects.all()
