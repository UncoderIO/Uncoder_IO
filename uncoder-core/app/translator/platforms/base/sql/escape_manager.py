from typing import ClassVar

from app.translator.core.escape_manager import EscapeManager
from app.translator.core.models.escape_details import EscapeDetails
from app.translator.platforms.base.sql.custom_types.values import SQLValueType


class SQLEscapeManager(EscapeManager):
    escape_map: ClassVar[dict[str, list[EscapeDetails]]] = {
        SQLValueType.value: [EscapeDetails(pattern=r"(')", escape_symbols=r"'\1")],
        SQLValueType.like_value: [EscapeDetails(pattern=r"(['%_\\])", escape_symbols=r"\\\1")],
        SQLValueType.regex_value: [
            EscapeDetails(pattern=r"([$^*+()\[\]{}|.?\-\\])", escape_symbols=r"\\\1"),
            EscapeDetails(pattern=r"(')", escape_symbols=r"'\1"),
        ],
    }


sql_escape_manager = SQLEscapeManager()
