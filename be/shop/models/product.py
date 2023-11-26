from decimal import Decimal
from django.db.models import (
    ForeignKey,
    Model,
    CASCADE,
    UUIDField,
    CharField,
    IntegerField,
    DecimalField,
    FloatField,
)
import uuid
from strenum import StrEnum
from enum import auto
from shop.enums import GAME_CATEGORIES



"""

Fieldname in Python | Name in PostgreSQL
CharField           | VARCHAR
IntegerField        | INTEGER
DecimalField        | DECIMAL
UUIDField           | UUID
TextField           | TEXT


OneToOneField is same as ForiegnKey
EmailField is same as CharField
CheckConstraint means CHECK

For Example - CHECK (age > 0) and (age <150) 


"""

class Product(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CharField(max_length=100)
    inventory = IntegerField(default=0)
    price = DecimalField(max_digits=10, decimal_places=2)
    category = CharField(
        max_length=20, choices=list(map(lambda x: (x.name, x.value), GAME_CATEGORIES))
    )
    original_cost = DecimalField(max_digits=10, decimal_places=2)
    store = ForeignKey("shop.Store", on_delete=CASCADE, null=False)
