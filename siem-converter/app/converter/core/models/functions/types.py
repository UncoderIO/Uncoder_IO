from enum import Enum, auto
from dataclasses import dataclass, field


class ComparsionType(Enum):
    EQUAL = auto()
    ILIKE = auto()
    NOT_EQUAL = auto()
    GTE = auto()
    LTE = auto()
    GT = auto()
    LT = auto()


class ModifierType(Enum):
    CONTAINS = auto()
    STARTSWITH = auto()
    ENDSWITH = auto()
    REGEX = auto()
    EQUAL = auto()


class OperatorType(Enum):
    AND = auto()
    OR = auto()
    NOT = auto()
    XOR = auto()


class AggregationType(Enum):
    SUM = auto()
    COUNT = auto()
    AVG = auto()
    MIN = auto()
    MAX = auto()
    MEDIAN = auto()
    DISTINCT_COUNT = auto()
    RANGE = auto()


class NotSupportedFunction:
    def __init__(self, name: str, query: str):
        self.name = name
        self.query = query


class SubFunc:
    def __init__(self, func_name: str, fieldname: str, values: list):
        self.func_name = func_name
        self.fieldname = fieldname
        self.values = values


@dataclass
class ParsedFunctions:
    functions: list = field(default_factory=list)
    not_supported: list = field(default_factory=list)
