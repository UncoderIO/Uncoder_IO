from typing import ClassVar

from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.models.escape_details import EscapeDetails


class LogRhythmQueryEscapeManager(EscapeManager):
    escape_map: ClassVar[dict[str, list[EscapeDetails]]] = {
        ValueType.value: [EscapeDetails(pattern=r"'", escape_symbols=r"''")],
        ValueType.regex_value: [
            EscapeDetails(pattern=r"\\", escape_symbols=r"\\\\"),
            EscapeDetails(pattern=r"\*", escape_symbols=r"\\*"),
            EscapeDetails(pattern=r"\.", escape_symbols=r"\\."),
            EscapeDetails(pattern=r"\^", escape_symbols=r"\\^"),
            EscapeDetails(pattern=r"\$", escape_symbols=r"\\$"),
            EscapeDetails(pattern=r"\|", escape_symbols=r"\\|"),
            EscapeDetails(pattern=r"\?", escape_symbols=r"\\?"),
            EscapeDetails(pattern=r"\+", escape_symbols=r"\\+"),
            EscapeDetails(pattern=r"\(", escape_symbols=r"\\("),
            EscapeDetails(pattern=r"\)", escape_symbols=r"\\)"),
            EscapeDetails(pattern=r"\[", escape_symbols=r"\\["),
            EscapeDetails(pattern=r"\]", escape_symbols=r"\\]"),
            EscapeDetails(pattern=r"\{", escape_symbols=r"\\{"),
            EscapeDetails(pattern=r"\}", escape_symbols=r"\\}"),
        ],
    }


class LogRhythmRuleEscapeManager(EscapeManager):
    escape_map: ClassVar[dict[str, list[EscapeDetails]]] = {
        ValueType.value: [EscapeDetails(pattern=r"'", escape_symbols=r"''")]
    }


logrhythm_query_escape_manager = LogRhythmQueryEscapeManager()
logrhythm_rule_escape_manager = LogRhythmRuleEscapeManager()
