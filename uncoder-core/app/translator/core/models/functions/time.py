from dataclasses import dataclass

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.custom_types.time import TimeFrameType
from app.translator.core.models.functions.base import Function


@dataclass
class TimeFrameFunction(Function):
    name: str = FunctionType.timeframe
    timeframe_value: str = "1"
    timeframe_type: str = TimeFrameType.days
