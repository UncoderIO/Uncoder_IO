import copy

from app.translator.core.str_value_manager import (
    CONTAINER_SPEC_SYMBOLS_MAP,
    SingleSymbolWildCard,
    StrValueManager,
    UnboundLenWildCard,
)
from app.translator.platforms.forti_siem.escape_manager import forti_siem_escape_manager

FORTI_CONTAINER_SPEC_SYMBOLS_MAP = copy.copy(CONTAINER_SPEC_SYMBOLS_MAP)
FORTI_CONTAINER_SPEC_SYMBOLS_MAP.update({SingleSymbolWildCard: ".?", UnboundLenWildCard: ".*"})


class FortiSiemStrValueManager(StrValueManager):
    escape_manager = forti_siem_escape_manager
    container_spec_symbols_map = FORTI_CONTAINER_SPEC_SYMBOLS_MAP


forti_siem_str_value_manager = FortiSiemStrValueManager()
