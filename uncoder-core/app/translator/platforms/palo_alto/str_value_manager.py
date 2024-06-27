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

from app.translator.core.custom_types.values import ValueType
from app.translator.core.str_value_manager import (
    CONTAINER_SPEC_SYMBOLS_MAP,
    BaseSpecSymbol,
    SingleSymbolWildCard,
    StrValue,
    StrValueManager,
    UnboundLenWildCard,
)
from app.translator.platforms.palo_alto.escape_manager import cortex_xql_escape_manager

CORTEX_XQL_CONTAINER_SPEC_SYMBOLS_MAP = copy.copy(CONTAINER_SPEC_SYMBOLS_MAP)
CORTEX_XQL_CONTAINER_SPEC_SYMBOLS_MAP.update({SingleSymbolWildCard: ".*", UnboundLenWildCard: ".*"})


class CortexXQLStrValueManager(StrValueManager):
    escape_manager = cortex_xql_escape_manager
    container_spec_symbols_map = CORTEX_XQL_CONTAINER_SPEC_SYMBOLS_MAP

    def from_container_to_str(self, container: StrValue, value_type: str = ValueType.value) -> str:
        result = ""
        for el in container.split_value:
            if isinstance(el, str):
                result += self.escape_manager.escape(el, value_type)
            elif isinstance(el, BaseSpecSymbol):
                if value_type == ValueType.value:
                    if isinstance(el, (SingleSymbolWildCard, UnboundLenWildCard)):
                        result += "*"
                elif pattern := self.container_spec_symbols_map.get(type(el)):
                    result += pattern

        return result


cortex_xql_str_value_manager = CortexXQLStrValueManager()
