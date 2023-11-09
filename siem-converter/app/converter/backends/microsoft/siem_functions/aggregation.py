from app.converter.core.models.functions.aggregation import AggregationExpression
from app.converter.core.models.functions.types import AggregationType


class AlaAggregationFunctionRender:

    aggregation_type_map = {
        AggregationType.SUM: 'sum',
        AggregationType.MIN: 'min',
        AggregationType.MAX: 'max',
        AggregationType.AVG: 'avg'
    }

    def __init__(self, function: AggregationExpression):
        self.function = function

    def render(self):
        result = 'summarize '
        for field in self.function.fields:
            if field.operation_type == AggregationType.COUNT:
                query = field.fieldname
            else:
                query = f"{self.aggregation_type_map.get(field.operation_type)}({field.fieldname})"
            if field.render_as:
                if ' ' in field.render_as:
                    render_as = f"['{field.render_as}']"
                else:
                    render_as = field.render_as
                result += f'{render_as}={query}, '
            else:
                result += query
        result = result.rstrip(' ').rstrip(',')
        if self.function.group_by:
            result += ' by '
        for value in self.function.group_by:
            result += f'{value}, '
        
        result = result.rstrip(' ').rstrip(',')

        return result
