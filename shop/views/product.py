from rest_framework.viewsets import ModelViewSet

from shop.models.product import Product
from shop.serializers import ProductSerializer

class ProductModelViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer