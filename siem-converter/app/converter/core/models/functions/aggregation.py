from app.converter.core.models.functions.types import AggregationType


class AggregationField:
    def __init__(
        self,
        fieldname: str,
        operation_type: AggregationType,
        render_as: str = None
    ):
        self.fieldname = fieldname
        self.operation_type = operation_type
        self.render_as = render_as
    
    def __repr__(self):
        base = f'{self.operation_type}:{self.fieldname}'
        if self.render_as:
            base += f' as {self.render_as}'
        return base


class AggregationExpression:
    def __init__(self):
        self.fields = []
        self.group_by = []
