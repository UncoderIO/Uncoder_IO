from contextvars import ContextVar

from app.translator.core.custom_types.functions import FunctionType
from app.translator.tools.custom_enum import CustomEnum


class AQLFunctionType(CustomEnum):
    lower: str = "LOWER"
    upper: str = "UPPER"
    min: str = "MIN"
    max: str = "MAX"
    sum: str = "SUM"
    avg: str = "AVG"
    count: str = "COUNT"
    distinct_count: str = "DISTINCTCOUNT"
    group_by: str = "GROUP BY"
    last: str = "LAST"
    fields: str = "SELECT"
    limit: str = "LIMIT"
    order_by: str = "ORDER BY"

    aggregation_data_function: str = "aggregation_data_function"


class AQLFunctionGroupType(CustomEnum):
    agg = "agg"


class AQLSortOrderType(CustomEnum):
    asc: str = "ASC"
    desc: str = "DESC"


class AQLTimeFrameType(CustomEnum):
    days = "DAYS"
    hours = "HOURS"
    minutes = "MINUTES"


func_aliases_ctx_var: ContextVar[list[str]] = ContextVar("func_aliases_ctx_var", default=[])


AGGREGATION_FUNCTIONS_MAP = {
    AQLFunctionType.avg: FunctionType.avg,
    AQLFunctionType.count: FunctionType.count,
    AQLFunctionType.distinct_count: FunctionType.distinct_count,
    AQLFunctionType.max: FunctionType.max,
    AQLFunctionType.min: FunctionType.min,
    AQLFunctionType.sum: FunctionType.sum,
}
