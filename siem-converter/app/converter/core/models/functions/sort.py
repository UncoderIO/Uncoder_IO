from enum import Enum, auto


class SortTransformType(Enum):
    INT = auto()
    STRING = auto()


class SortOrderType(Enum):
    ASC = auto()
    DESC = auto()


class SortField:
    def __init__(self, fieldname: str, order: SortOrderType = SortOrderType.ASC, transform_into: SortTransformType = None):
        self.fieldname = fieldname
        self.order = order
        self.transform_into = transform_into


class SortExpression:
    def __init__(self, count: int = 10_000, order: str = SortOrderType.DESC):
        self.count = count
        self.order = order
        self.fields = []
        self.is_count_default = True

    def set_count(self, value):
        self.is_count_default = False
        self.count = value

    def is_default_count(self):
        return self.is_count_default
