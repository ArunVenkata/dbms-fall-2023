from decimal import Decimal
from django.db.models import CharField, UUIDField, IntegerField, CheckConstraint, Q, DecimalField, TextField
from django.contrib.auth.models import AbstractUser
from strenum import StrEnum
from enum import auto
from django.db.models import Model, ForeignKey, SET_NULL
from uuid import uuid4


class Region(Model):
    id = UUIDField(primary_key=True, default = uuid4())
    name = CharField(max_length=200)
    manager = ForeignKey("userauth.User", on_delete=SET_NULL, null=True)