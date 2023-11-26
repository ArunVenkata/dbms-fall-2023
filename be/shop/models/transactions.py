from decimal import Decimal
from django.db.models import CharField, UUIDField, IntegerField, CheckConstraint, Q, DecimalField, TextField, OneToOneField
from django.contrib.auth.models import AbstractUser
from strenum import StrEnum
from enum import auto
from django.db.models import Model, ForeignKey, SET_NULL, CASCADE
from uuid import uuid4

from shop.enums import GAME_CATEGORIES

class UserTransaction(Model):
    id = UUIDField(primary_key=True, default = uuid4)
    purchased_by = ForeignKey("userauth.User", on_delete=CASCADE)
    product = ForeignKey("shop.Product", on_delete=SET_NULL, null=True)
    salesperson = ForeignKey("userauth.SalesUser", on_delete=SET_NULL, null=True)
    name = CharField(max_length=100)
    price = DecimalField(default=Decimal,max_digits=10, decimal_places=2)
    category = CharField(max_length=20, choices=list(map(lambda x: (x.name, x.value), GAME_CATEGORIES)))
    quantity = IntegerField()
    comments = TextField(default=str)
    
    class Meta:
            constraints = [
                CheckConstraint(
                    name="%(app_label)s_%(class)s_quantity_range",
                    check=Q(quantity__range=(1,1000)),
                ),
            ]
