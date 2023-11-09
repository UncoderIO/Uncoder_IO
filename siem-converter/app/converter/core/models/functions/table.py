from app.converter.core.operator_types.tokens import OperatorType


class TableField:
    def __init__(self, fieldname: str, raw_fieldname: str, modifier: OperatorType = OperatorType.EQ):
        self.fieldname = fieldname
        self.raw_fieldname = raw_fieldname
        self.modifier = modifier


class TableExpression:
    def __init__(self):
        self.fields = []
