from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager
from app.translator.core.models.escape_details import EscapeDetails


class LuceneEscapeManager(EscapeManager):
    escape_map = {
        ValueType.value: EscapeDetails(pattern=r'([_!@#$%^&*=+()\[\]{}|;:\'",.<>?/`~\-\s\\])', escape_symbols=r"\\\1")
    }


lucene_escape_manager = LuceneEscapeManager()
