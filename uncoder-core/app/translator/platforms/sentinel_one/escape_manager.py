from typing import ClassVar

from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.models.escape_details import EscapeDetails
from app.translator.platforms.sentinel_one.custom_types.values import SentinelOneValueType


class SentinelOnePowerQueryEscapeManager(EscapeManager):
    escape_map: ClassVar[dict[str, list[EscapeDetails]]] = {
        ValueType.value: [EscapeDetails(pattern=r"\\", escape_symbols=r"\\\\")],
        ValueType.regex_value: [EscapeDetails(pattern=r"([$^*+()\[\]{}|.?\-\\])", escape_symbols=r"\\\1")],
        SentinelOneValueType.double_escape_regex_value: [EscapeDetails(pattern=r"\\", escape_symbols=r"\\\\")],
    }


sentinel_one_power_query_escape_manager = SentinelOnePowerQueryEscapeManager()
