from decimal import Decimal
from django.db.models import CharField, UUIDField, IntegerField, CheckConstraint, Q, DecimalField, OneToOneField
from django.contrib.auth.models import AbstractUser
from strenum import StrEnum
from enum import auto
from django.db.models import Model, ForeignKey, CASCADE, SET_NULL
from uuid import uuid4

from userauth.enums import *

class User(AbstractUser):
    id = UUIDField(primary_key=True, default = uuid4())
    user_type = CharField(choices=list(map(lambda x: (x.name, x.value),USER_TYPES)), null=False)



class Address(Model):
    id = OneToOneField("User", on_delete=CASCADE, primary_key=True)
    state = CharField(max_length=100)
    zip_code = CharField(max_length=10)
    street = CharField(max_length=200)
    city = CharField(max_length=200)

class BusinessUser(Model):
    id = OneToOneField("User", on_delete=CASCADE, primary_key=True)
    business_category = CharField(max_length=100)
    gross_annual_income= DecimalField(max_digits=20, decimal_places=2,default=Decimal)



class HomeUser(Model):
    id = OneToOneField("User", on_delete=CASCADE, primary_key=True)
    marital_status = CharField(choices=list(map(lambda x: (x.name, x.value),MARITAL_STATUSES)), null=False)
    gender = CharField(default=str)
    age = IntegerField()
    income = DecimalField(max_digits=20, decimal_places=2, default=Decimal)


    class Meta:
            constraints = [
                CheckConstraint(
                    name="%(app_label)s_%(class)s_age_range",
                    check=Q(age__range=(18, 150)),
                )
            ]


class SalesUser(Model):
    id = OneToOneField("User", on_delete=CASCADE, primary_key=True)
    job_title = CharField(max_length=150)
    store_assigned = ForeignKey("shop.Store", on_delete=SET_NULL, null=True)
    income = DecimalField(max_digits=20, decimal_places=2, default=Decimal)

