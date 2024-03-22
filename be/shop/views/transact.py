from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from shop.serializers import UserTransactionHistorySerializer
from shop.models import Product, UserTransaction, UserTransactionDetails
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F


def validate_cart(cart: dict):
    valid_products = Product.objects.filter(id__in=set(cart.keys())).values(
        "id", "inventory", "price", "name", 
    )

    valid_products_d = {f"{item['id']}": item for item in valid_products}
    print(valid_products_d, "VALID D")
    invalid_product_ids = set()
    valid_product_ids = set()
    for productId, product_data in cart.items():
        print(productId, product_data, "---")
        if productId not in valid_products_d:
            invalid_product_ids.add(productId)
            continue
        if product := valid_products_d.get(productId):
            print("PRODUCT: ", product)
            if product_data["quantity"] > product["inventory"]:
                invalid_product_ids.add(productId)
                continue
            if Decimal(str(product_data["cost"])) != product["price"]:
                invalid_product_ids.add(productId)
                continue
            valid_product_ids.add(productId)

    valid_products_d = {key: {**cart[key], **valid_products_d[key]} for key in valid_product_ids}

    return valid_products_d, bool(invalid_product_ids)


def reduce_inventory(product_id_qty_map):
    with transaction.atomic():
        for product_id, quantity_used in product_id_qty_map.items():
            Product.objects.filter(id=product_id).update(inventory=F("inventory")-quantity_used)

            


class TransactView(APIView):
    """
    User clicks checkout

    Data for transaction gets sent here

    Data is validated

    Transaction Added to the database

    Success response

    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = request.data.get("cart")
        salesperson_id = request.data.get("salesperson_id")
        new_cart, success = validate_cart(cart)

        if not new_cart:
            return Response({"success": False, "message": "Invalid Cart"})

        print(new_cart, "NEW CART")
        print(salesperson_id, "salesperson ID")
        product_id_qty_map = {}
        with transaction.atomic():
            # Create Transaction
            txn = UserTransaction.objects.create(
                purchased_by_id=request.user.id, salesperson_id=salesperson_id
            )
            _txn_details_data = [
                
                
            ]
            
            for product_id, product_data in new_cart.items():
                _txn_details_data.append(UserTransactionDetails(**{
                    "transaction_id": str(txn.id),
                    "name": product_data["name"],
                    "product_id": product_id,
                    "price": Decimal(f"{product_data['price']}"),
                    "quantity": product_data["quantity"],
                }))
                product_id_qty_map[product_id] = product_data["quantity"]

            UserTransactionDetails.objects.bulk_create(_txn_details_data)
        reduce_inventory(product_id_qty_map)
            # Create transaction details using given transaction
        return Response({"success": True})




class TransactionHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        data = UserTransactionHistorySerializer(UserTransaction.objects.filter(purchased_by_id=request.user.id), many=True).data
        return Response(data)