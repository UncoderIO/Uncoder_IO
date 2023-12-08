from abc import ABC

from app.translator.core.custom_types.tokens import LogicalOperatorType


class BaseOperator(ABC):
    token_type: str = None

    def __init__(self, items=None):
        self.items = [] if items is None else items

    def __add__(self, other):
        if isinstance(other, list):
            self.items.extend(other)
        else:
            self.items.append(other)
        return self

    def __repr__(self):
        return f"{self.token_type}({self.items})"

    def remove_last_item(self):
        self.items = self.items[:-1]


class AND(BaseOperator):
    token_type = LogicalOperatorType.AND


class OR(BaseOperator):
    token_type = LogicalOperatorType.OR


class NOT(BaseOperator):
    token_type = LogicalOperatorType.NOT

    def __add__(self, other):
        self.items = other
        return self


class Operator:
    def __new__(cls, operator_type, items=None):
        if operator_type == LogicalOperatorType.AND:
            return AND()
        elif operator_type == LogicalOperatorType.OR:
            return OR()
        elif operator_type == LogicalOperatorType.NOT:
            return NOT(items)
        return None
