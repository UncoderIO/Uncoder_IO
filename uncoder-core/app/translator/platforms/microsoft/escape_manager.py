from typing import ClassVar

from app.translator.core.escape_manager import EscapeManager
from app.translator.core.models.escape_details import EscapeDetails
from app.translator.platforms.microsoft.custom_types.values import KQLValueType


class MicrosoftKQLEscapeManager(EscapeManager):
    escape_map: ClassVar[dict[str, list[EscapeDetails]]] = {
        KQLValueType.verbatim_single_quotes_value: [EscapeDetails(pattern=r"(')", escape_symbols=r"'\1")],
        KQLValueType.verbatim_double_quotes_regex_value: [
            EscapeDetails(pattern=r"([$^*+()\[\]{}|.?\-\\])", escape_symbols=r"\\\1")
        ],
        KQLValueType.verbatim_single_quotes_regex_value: [
            EscapeDetails(pattern=r"([$^*+()\[\]{}|.?\-\\])", escape_symbols=r"\\\1")
        ],
        KQLValueType.single_quotes_regex_value: [
            EscapeDetails(pattern=r"([$^*+()\[\]{}|.?\-])", escape_symbols=r"\\\\\1"),
            EscapeDetails(pattern=r"(\\(?![$^*+()\[\]{}|.?\-\\]))", escape_symbols=r"[\\\\\\\1]"),
            EscapeDetails(pattern=r"(')", escape_symbols=r"[\\\1]"),
        ],
    }


microsoft_kql_escape_manager = MicrosoftKQLEscapeManager()
