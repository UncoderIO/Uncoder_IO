from app.translator.core.escape_manager import EscapeManager


class QradarEscapeManager(EscapeManager):
    escape_map = {}


qradar_escape_manager = QradarEscapeManager()
