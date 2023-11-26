from rest_framework.viewsets import ModelViewSet
from shop.models.store import Store
from shop.serializers import StoreSerializer
from rest_framework.permissions import IsAuthenticated


class StoreModelViewSet(ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission_classes = [IsAuthenticated]
