from rest_framework.serializers import (
    ModelSerializer,
    ValidationError as SerializerValidationError,
)
from shop.models.transactions import UserTransaction, UserTransactionDetails

from shop.models.product import Product
from shop.models.region import Region
from shop.models.store import Store
from utilities import DynamicFieldsModelSerializer, is_valid_uuid
from django.db.models.aggregates import Sum
from django.db.models import F


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
        if "manager" in data and data["manager"]:
            data["manager"] = UserViewsetSerializer(
                User.objects.get(id=data["manager"]),
                exclude=["current_region", "created_at"],
            ).data
        pq = Product.objects.filter(store_id=data["id"], inventory__gte=1)
        if self.context and self.context.get('request') and (query_product_name:=self.context['request'].query_params.get("product_name")):
            print("Prod name", query_product_name)
            pq = pq.filter(name__icontains=query_product_name)
        data["products"] = ProductSerializer(
            pq, many=True
        ).data
        return data


class RegionSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Region


class UserTransactionHistorySerializer(DynamicFieldsModelSerializer):
    class Meta:
        fields = (
            "id",
            "purchased_by",
            "salesperson",
            "comments",
            "usertransactiondetails_set",
        )
        model = UserTransaction

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["total_order_value"] = UserTransactionDetails.objects.filter(
            transaction_id=data["id"]
        ).aggregate(total=Sum(F("price") * F("quantity")))['total']
        return data
