from app.converter.core.models.functions.search import SearchExpression, SearchField, SearchValueType
from app.converter.core.models.functions.types import ComparsionType
from app.converter.core.operator_types.tokens import LogicalOperatorType


class AlaSearchFunctionRender:
    
    search_expression_operator_map = {
        LogicalOperatorType.AND: ' and ',
        LogicalOperatorType.OR: ' or ',
        LogicalOperatorType.NOT: ' not '
    }
    search_operator_map = {
        ComparsionType.NOT_EQUAL: ' != ',
        ComparsionType.EQUAL: '==',
        ComparsionType.ILIKE: ':',
        ComparsionType.GT: ' > ',
        ComparsionType.LT: ' < '
    }
    sub_expression = "(%s)"

    def __init__(self, function: SearchExpression):
        self.function = function

    def generate_field(self, field: SearchField):
        if field.value == SearchValueType.ANY:
            return f'"{field.fieldname}"'
        else:
            if field.fieldname:
                operator = self.search_operator_map.get(field.operator)
                return f'{field.fieldname}{operator}"{field.value}"'
            else:
                return f'"{field.value}"'
    
    def generate_expression(self, expression: SearchExpression):
        res = []
        for field in expression.fields:
            if isinstance(field, SearchField):
                res.append(self.generate_field(field))
            elif isinstance(field, SearchExpression):
                res.append(self.generate_expression(field))
        operator = self.search_expression_operator_map.get(expression.operator)
        query = self.sub_expression % operator.join(res)
        if expression.operator == LogicalOperatorType.NOT:
            return f'not{query}'
        return query

    def render(self):
        res = []
        for field in self.function.fields:
            if isinstance(field, SearchField):
                res.append(self.generate_field(field))
            elif isinstance(field, SearchExpression):
                res.append(self.generate_expression(field))
        operator = self.search_expression_operator_map.get(self.function.operator)
        return f'search {operator.join(res)}'
