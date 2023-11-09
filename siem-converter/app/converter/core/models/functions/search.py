from enum import Enum, auto

from app.converter.core.models.functions.types import ComparsionType, ModifierType, OperatorType


class SearchValueType(Enum):
    ANY = auto()


class SearchField:
    def __init__(
        self,
        fieldname: str,
        value: [str, SearchValueType],
        operator: ComparsionType,
        modifier: [None, ModifierType] = None,
        case_sensitive: bool = False,
        full_match: bool = False
    ):
        self.operator = operator
        self.fieldname = fieldname
        self.value = value
        self.modifier = modifier
        self.case_sensitive = case_sensitive
        self.full_match = full_match


class SearchExpression:
    def __init__(self, operator: OperatorType, fields: list, case_sensitive: bool = False):
        self.operator = operator
        self.fields = fields
        self.case_sensitive = case_sensitive
