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
from typing import ClassVar

from app.translator.core.str_value_manager import (
    BaseSpecSymbol,
    ReAnySymbol,
    ReCaretSymbol,
    ReCommaSymbol,
    ReHyphenSymbol,
    ReLeftCurlyBracket,
    ReLeftParenthesis,
    ReLeftSquareBracket,
    ReOneOrMoreQuantifier,
    ReOrOperator,
    ReRightCurlyBracket,
    ReRightParenthesis,
    ReRightSquareBracket,
    ReZeroOrMoreQuantifier,
    ReZeroOrOneQuantifier,
    SingleSymbolWildCard,
    StrValue,
    StrValueManager,
    UnboundLenWildCard,
)
from app.translator.platforms.base.lucene.escape_manager import lucene_escape_manager

RE_STR_SPEC_SYMBOLS_MAP = {
    "?": ReZeroOrOneQuantifier,
    "*": ReZeroOrMoreQuantifier,
    "+": ReOneOrMoreQuantifier,
    ".": ReAnySymbol,
    "[": ReLeftSquareBracket,
    "]": ReRightSquareBracket,
    "(": ReLeftParenthesis,
    ")": ReRightParenthesis,
    "{": ReLeftCurlyBracket,
    "}": ReRightCurlyBracket,
    "|": ReOrOperator,
    "^": ReCaretSymbol,
    ",": ReCommaSymbol,
    "-": ReHyphenSymbol,
}


class LuceneStrValueManager(StrValueManager):
    escape_manager = lucene_escape_manager
    str_spec_symbols_map: ClassVar[dict[str, type[BaseSpecSymbol]]] = {
        "?": SingleSymbolWildCard,
        "*": UnboundLenWildCard,
    }
    re_str_spec_symbols_map = RE_STR_SPEC_SYMBOLS_MAP

    def from_str_to_container(self, value: str) -> StrValue:
        split = []
        prev_char = None
        for char in value:
            if char == "\\":
                if prev_char == "\\":
                    split.append(char)
                    prev_char = None
                    continue
            elif char in self.str_spec_symbols_map:
                if prev_char == "\\":
                    split.append(char)
                else:
                    split.append(self.str_spec_symbols_map[char]())
            else:
                split.append(char)

            prev_char = char

        return StrValue(value, self._concat(split))


lucene_str_value_manager = LuceneStrValueManager()
