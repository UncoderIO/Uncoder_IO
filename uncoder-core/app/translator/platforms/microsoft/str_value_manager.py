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
import re
from typing import Optional

from app.translator.core.str_value_manager import (
    CONTAINER_SPEC_SYMBOLS_MAP,
    RE_STR_ALPHA_NUM_SYMBOLS_MAP,
    RE_STR_SPEC_SYMBOLS_MAP,
    BaseSpecSymbol,
    SingleSymbolWildCard,
    StrValue,
    StrValueManager,
    UnboundLenWildCard,
)
from app.translator.platforms.microsoft.custom_types.values import KQLValueType
from app.translator.platforms.microsoft.escape_manager import microsoft_kql_escape_manager

KQL_CONTAINER_SPEC_SYMBOLS_MAP = copy.copy(CONTAINER_SPEC_SYMBOLS_MAP)
KQL_CONTAINER_SPEC_SYMBOLS_MAP.update({SingleSymbolWildCard: ".?", UnboundLenWildCard: ".*"})


class MicrosoftKQLStrValueManager(StrValueManager):
    escape_manager = microsoft_kql_escape_manager
    container_spec_symbols_map = KQL_CONTAINER_SPEC_SYMBOLS_MAP
    re_str_alpha_num_symbols_map = RE_STR_ALPHA_NUM_SYMBOLS_MAP
    re_str_spec_symbols_map = RE_STR_SPEC_SYMBOLS_MAP

    def from_str_to_container(
        self,
        value: str,
        value_type: str = KQLValueType.value,
        escape_symbol: Optional[str] = None,  # noqa: ARG002
    ) -> StrValue:
        if value_type == KQLValueType.verbatim_single_quotes_value:
            return self.__from_verbatim_str_to_container(value, quote_char="'")

        if value_type == KQLValueType.verbatim_double_quotes_value:
            return self.__from_verbatim_str_to_container(value, quote_char='"')

        if value_type == KQLValueType.single_quotes_value:
            return self.__from_str_to_container(value, quote_char="'")

        return self.__from_str_to_container(value, quote_char='"')

    def __from_str_to_container(self, value: str, quote_char: str) -> StrValue:
        split = []
        prev_char = None

        for char in value:
            if char in ("\\", quote_char):
                if prev_char == "\\":
                    split.append(char)
                    prev_char = None
                    continue
            else:
                split.append(char)

            prev_char = char

        return StrValue(value, self._concat(split))

    def __from_verbatim_str_to_container(self, value: str, quote_char: str) -> StrValue:
        split = []
        prev_char = None

        for char in value:
            if char != quote_char:
                split.append(char)
            elif char == prev_char:
                split.append(char)
                prev_char = None
                continue

            prev_char = char

        return StrValue(value, self._concat(split))

    def from_re_str_to_container(self, value: str, value_type: str = KQLValueType.regex_value) -> StrValue:
        if value_type in (KQLValueType.single_quotes_regex_value, KQLValueType.double_quotes_regex_value):
            value = re.sub(r"\[\\\"]", r'"', value)
            value = re.sub(r"\[\\\']", r"'", value)
            value = re.sub(r"\\\\", r"\\", value)
            value = re.sub(r"\[\\\\]", r"\\\\", value)

        return super().from_re_str_to_container(value, value_type)

    def from_container_to_str(self, container: StrValue, value_type: str = KQLValueType.value) -> str:
        result = ""
        for el in container.split_value:
            if isinstance(el, str):
                result += self.escape_manager.escape(el, value_type)
            elif isinstance(el, BaseSpecSymbol) and (pattern := self.container_spec_symbols_map.get(type(el))):
                if value_type == KQLValueType.single_quotes_regex_value and "\\" in pattern:
                    pattern = rf"\{pattern}"
                result += pattern

        return result


microsoft_kql_str_value_manager = MicrosoftKQLStrValueManager()
