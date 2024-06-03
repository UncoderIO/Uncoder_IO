from contextvars import ContextVar

from app.translator.core.custom_types.functions import FunctionType
from app.translator.platforms.base.aql.functions import AQLFunctionType
from app.translator.tools.custom_enum import CustomEnum


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
