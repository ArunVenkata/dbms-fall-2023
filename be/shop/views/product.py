from rest_framework.viewsets import ModelViewSet

from shop.models.product import Product
from shop.models.region import Region
from shop.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ProductModelViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method.lower() == "get":
            regionquery = Region.objects
            if region := self.request.query_params.get("region"):
                regionquery = regionquery.filter(name=region)
            region = regionquery.first()
            if not region:
                return queryset.filter(store__region__name="___")
            region = region.name
            queryset = queryset.filter(store__region__name=region)
        return queryset

    def list(self, request, *args, **kwargs):
        
        return Response({"success": True, "data":super().list(request, *args, **kwargs).data })
