from decimal import Decimal
from django.db.models import Model, UUIDField, CharField, IntegerField,DecimalField, FloatField
import uuid
from strenum import StrEnum
from enum import auto

class GAME_CATEGORIES(StrEnum):
    board_game = auto()
    card_game = auto()
    video_game = auto()
    war_games = auto()
    adventure = auto()
    


class Product(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CharField(max_length=100)
    inventory = IntegerField(default=0)
    price = DecimalField(default=Decimal('0.00'),max_digits=10, decimal_places=2)
    category = CharField(max_length=20, choices=list(map(lambda x: (x.name, x.value),GAME_CATEGORIES)))


