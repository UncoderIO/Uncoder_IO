from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.models.escape_details import EscapeDetails


class ChronicleEscapeManager(EscapeManager):
    escape_map = {
        ValueType.value: EscapeDetails(pattern='([\\\\|"])'),
        ValueType.regular_expression_value: EscapeDetails(pattern='([\\\\|/(")\\[\\]{}.^$+<>!?])')
    }


chronicle_escape_manager = ChronicleEscapeManager()
