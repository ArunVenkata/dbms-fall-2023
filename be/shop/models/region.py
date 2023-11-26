from django.db.models import CharField, UUIDField
from django.db.models import Model, ForeignKey, SET_NULL
from uuid import uuid4

class Region(Model):
    id = UUIDField(primary_key=True, default = uuid4)
    name = CharField(max_length=200)
    manager = ForeignKey("userauth.User", on_delete=SET_NULL, null=True)