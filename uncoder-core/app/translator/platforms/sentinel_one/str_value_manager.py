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
from app.translator.core.custom_types.values import ValueType
from app.translator.core.str_value_manager import BaseSpecSymbol, StrValue, StrValueManager
from app.translator.platforms.sentinel_one.custom_types.values import SentinelOneValueType
from app.translator.platforms.sentinel_one.escape_manager import (
    SentinelOnePowerQueryEscapeManager,
    sentinel_one_power_query_escape_manager,
)


class SentinelOnePowerQueryStrValueManager(StrValueManager):
    escape_manager: SentinelOnePowerQueryEscapeManager = sentinel_one_power_query_escape_manager

    def from_container_to_str(self, container: StrValue, value_type: str = ValueType.value) -> str:
        result = ""
        for el in container.split_value:
            if isinstance(el, str):
                result += self.escape_manager.escape(el, value_type)
            elif isinstance(el, BaseSpecSymbol) and (pattern := self.container_spec_symbols_map.get(type(el))):
                if value_type == ValueType.regex_value:
                    pattern = self.escape_manager.escape(pattern, SentinelOneValueType.double_escape_regex_value)
                result += pattern

        return result


sentinel_one_power_query_str_value_manager = SentinelOnePowerQueryStrValueManager()
