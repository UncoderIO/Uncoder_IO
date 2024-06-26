"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2024 SOC Prime, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------
"""

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
