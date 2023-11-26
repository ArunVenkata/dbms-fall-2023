from rest_framework.viewsets import ModelViewSet
from shop.models.region import Region
from shop.serializers import RegionSerializer
from rest_framework.permissions import IsAuthenticated


class RegionModelViewSet(ModelViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    permission_classes = [IsAuthenticated]
    