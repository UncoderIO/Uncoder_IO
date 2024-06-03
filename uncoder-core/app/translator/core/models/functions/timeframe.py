from dataclasses import dataclass

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.models.functions.base import Function
from app.translator.tools.custom_enum import CustomEnum


class TimeFrameType(CustomEnum):
    days = "days"
    hours = "hours"
    minutes = "minutes"


@dataclass
class TimeFrameFunction(Function):
    name: str = FunctionType.timeframe
    timeframe_value: str = "1"
    timeframe_type: str = TimeFrameType.days
