from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.models.escape_details import EscapeDetails


class QradarEscapeManager(EscapeManager):
    escape_map = {
        ValueType.value: EscapeDetails(pattern="([\\\])")
    }


qradar_escape_manager = QradarEscapeManager()
