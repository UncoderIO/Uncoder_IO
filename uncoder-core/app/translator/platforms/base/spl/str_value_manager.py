"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2023 SOC Prime, Inc.

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
from typing import ClassVar

from app.translator.core.str_value_manager import BaseSpecSymbol, StrValue, StrValueManager, UnboundLenWildCard
from app.translator.platforms.base.spl.escape_manager import spl_escape_manager


class SplStrValueManager(StrValueManager):
    escape_manager = spl_escape_manager
    str_spec_symbols_map: ClassVar[dict[str, type[BaseSpecSymbol]]] = {"*": UnboundLenWildCard}

    def from_str_to_container(self, value: str) -> StrValue:
        split = []
        prev_char = None
        for char in value:
            if char == "\\":
                if prev_char == "\\":
                    split.append("\\")
                    prev_char = None
                    continue
            elif char in self.str_spec_symbols_map:
                if prev_char == "\\":
                    split.append(char)
                else:
                    split.append(self.str_spec_symbols_map[char]())
            elif char in ('"', "=", "|", "<", ">"):
                split.append(char)
            else:
                if prev_char == "\\":
                    split.append(prev_char)
                split.append(char)

            prev_char = char

        return StrValue(self.escape_manager.remove_escape(value), self._concat(split))


spl_str_value_manager = SplStrValueManager()
