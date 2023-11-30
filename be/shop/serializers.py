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


    def to_representation(self, instance):
        data = super().to_representation(instance)
        from userauth.models import User
        from userauth.serializers import UserViewsetSerializer
        print(data["manager"], "MANAGGER")
        if "manager" in data and data["manager"]:
            data["manager"] = UserViewsetSerializer(User.objects.get(id=data["manager"]), exclude=["current_region", "created_at"]).data
        data["products"] = ProductSerializer(Product.objects.filter(store_id=data['id']), many=True).data
        return data

class RegionSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Region
