from rest_framework.serializers import ModelSerializer, ValidationError as SerializerValidationError

from shop.models.product import Product
from shop.models.region import Region
from shop.models.store import Store
from utilities import is_valid_uuid


class ProductSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Product


class StoreSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Store

    def to_internal_value(self, data):
        if "region" in data:
            region = data["region"]
            if is_valid_uuid(region):
                if not Region.objects.filter(id=region).exists():
                    raise SerializerValidationError("Invalid Region ID")
            region = Region.objects.filter(name=region).first()
            if region:
                data["region"] = str(region.id)

        return super().to_internal_value(data)


class RegionSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Region
