from typing import ClassVar

from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.models.escape_details import EscapeDetails


class FalcoRuleEscapeManager(EscapeManager):
    escape_map: ClassVar[dict[str, list[EscapeDetails]]] = {
        ValueType.regex_value: [
            EscapeDetails(pattern=r"([$^*+()\[\]{}|.?\-\\])", escape_symbols=r"\\\1"),
            EscapeDetails(pattern=r"(')", escape_symbols=r"'\1"),
        ]
    }


falco_rule_escape_manager = FalcoRuleEscapeManager()
