from typing import ClassVar

from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.models.escape_details import EscapeDetails


class FortiSiemEscapeManager(EscapeManager):
    escape_map: ClassVar[dict[str, list[EscapeDetails]]] = {
        ValueType.regex_value: [EscapeDetails(pattern=r'([*\\.()\[\]|{}^$+!?"])')]
    }


forti_siem_escape_manager = FortiSiemEscapeManager()
