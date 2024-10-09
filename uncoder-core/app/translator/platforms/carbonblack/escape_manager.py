from typing import ClassVar

from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.models.escape_details import EscapeDetails


class CarbonBlackEscapeManager(EscapeManager):
    escape_map: ClassVar[dict[str, list[EscapeDetails]]] = {
        ValueType.value: [
            EscapeDetails(
                pattern='([\s+\\-=&?!|(){}.\\[\\]^"~:/]|(?<!\\\\)\\\\(?![*?\\\\])|\\\\u|&&|\\|\\|)',
                escape_symbols="\\\\\g<1>",
            )
        ],
        ValueType.regex_value: [EscapeDetails(pattern=r"([$^*+()\[\]{}|.?\-\\])", escape_symbols=r"\\\1")],
    }


carbon_black_escape_manager = CarbonBlackEscapeManager()
