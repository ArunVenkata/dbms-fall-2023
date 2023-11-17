from strenum import StrEnum
from enum import auto


class USER_TYPES(StrEnum):
    home = auto()
    business = auto()
    salesperson = auto()

class MARITAL_STATUSES(StrEnum):
    unmarried = auto()
    married = auto()