from typing import ClassVar

from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.models.escape_details import EscapeDetails


class LogscaleEscapeManager(EscapeManager):
    escape_map: ClassVar[dict[str, list[EscapeDetails]]] = {
        ValueType.value: [EscapeDetails(pattern='(\\\\|/|\+|{|\[|\?|\*|"|\(|\))')]
    }


logscale_escape_manager = LogscaleEscapeManager()
