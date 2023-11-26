from decimal import Decimal
from django.db.models import CharField, UUIDField, IntegerField, CheckConstraint, Q, DecimalField, TextField
from django.contrib.auth.models import AbstractUser
from strenum import StrEnum
from enum import auto
from django.db.models import Model, ForeignKey, SET_NULL, CASCADE
from uuid import uuid4



class Store(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField(max_length=150)
    address = TextField()
    manager = ForeignKey("userauth.User", on_delete=SET_NULL, null=True)
    region = ForeignKey("Region", on_delete=CASCADE)
