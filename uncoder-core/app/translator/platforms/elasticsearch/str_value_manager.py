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
from typing import ClassVar, Optional

from app.translator.core.custom_types.values import ValueType
from app.translator.core.str_value_manager import (
    BaseSpecSymbol,
    ReDigitalSymbol,
    ReWhiteSpaceSymbol,
    ReWordSymbol,
    SingleSymbolWildCard,
    StrValue,
    StrValueManager,
)
from app.translator.platforms.elasticsearch.escape_manager import ESQLQueryEscapeManager, esql_query_escape_manager


class ESQLStrValueManager(StrValueManager):
    escape_manager: ESQLQueryEscapeManager = esql_query_escape_manager
    re_str_alpha_num_symbols_map: ClassVar[dict[str, type[BaseSpecSymbol]]] = {
        "w": ReWordSymbol,
        "d": ReDigitalSymbol,
        "s": ReWhiteSpaceSymbol,
    }


class EQLStrValueManager(StrValueManager):
    str_spec_symbols_map: ClassVar[dict[str, type[BaseSpecSymbol]]] = {"*": SingleSymbolWildCard}

    def from_str_to_container(
        self,
        value: str,
        value_type: str = ValueType.value,  # noqa: ARG002
        escape_symbol: Optional[str] = None,  # noqa: ARG002
    ) -> StrValue:
        split = [self.str_spec_symbols_map[char]() if char in self.str_spec_symbols_map else char for char in value]
        return StrValue(value, self._concat(split))


esql_str_value_manager = ESQLStrValueManager()
eql_str_value_manager = EQLStrValueManager()
