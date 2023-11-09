from app.converter.backends.microsoft.const import MICROSOFT_SENTINEL_QUERY_DETAILS
from app.converter.core.exceptions.render import FunctionRenderException
from app.converter.core.models.functions.table import TableExpression
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.operator_types.tokens import OperatorType


class AlaTableFunctionRender:
    details: PlatformDetails = PlatformDetails(**MICROSOFT_SENTINEL_QUERY_DETAILS)

    def __init__(self, function: TableExpression):
        self.function = function
    
    def render(self):
        result = "project "
        queries = []
        for field in self.function.fields:
            if field.operator != OperatorType.EQ:
                raise FunctionRenderException(
                    f'{self.details.name}: operator "project" not support modifier "{str(field.operator).split(".")[-1]}" in "{field.raw_fieldname}"'
                )
            queries.append(f"{field.fieldname}")
        result += ", ".join(queries)
        return result