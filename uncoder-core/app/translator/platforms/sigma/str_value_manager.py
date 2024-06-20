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

from app.translator.core.str_value_manager import (
    ReAnySymbol,
    ReCaretSymbol,
    ReCommaSymbol,
    ReDigitalSymbol,
    ReEndOfStrSymbol,
    ReHyphenSymbol,
    ReLeftCurlyBracket,
    ReLeftParenthesis,
    ReLeftSquareBracket,
    ReOneOrMoreQuantifier,
    ReOrOperator,
    ReRightCurlyBracket,
    ReRightParenthesis,
    ReRightSquareBracket,
    ReWhiteSpaceSymbol,
    ReWordSymbol,
    ReZeroOrMoreQuantifier,
    ReZeroOrOneQuantifier,
    SingleSymbolWildCard,
    StrValue,
    StrValueManager,
    UnboundLenWildCard,
)
from app.translator.platforms.sigma.escape_manager import sigma_escape_manager

RE_STR_SPEC_SYMBOLS_MAP = {
    "?": ReZeroOrOneQuantifier,
    "*": ReZeroOrMoreQuantifier,
    "+": ReOneOrMoreQuantifier,
    "^": ReCaretSymbol,
    "$": ReEndOfStrSymbol,
    ".": ReAnySymbol,
    "[": ReLeftSquareBracket,
    "]": ReRightSquareBracket,
    "(": ReLeftParenthesis,
    ")": ReRightParenthesis,
    "{": ReLeftCurlyBracket,
    "}": ReRightCurlyBracket,
    "|": ReOrOperator,
    ",": ReCommaSymbol,
    "-": ReHyphenSymbol,
}


class SigmaStrValueManager(StrValueManager):
    escape_manager = sigma_escape_manager
    str_spec_symbols_map = {"?": SingleSymbolWildCard, "*": UnboundLenWildCard}
    re_str_alpha_num_symbols_map = {"w": ReWordSymbol, "d": ReDigitalSymbol, "s": ReWhiteSpaceSymbol}
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
                if prev_char == "\\":
                    split.append(prev_char)
                split.append(char)

            prev_char = char

        if prev_char == "\\":
            split.append(prev_char)

        return StrValue(value, self._concat(split))


sigma_str_value_manager = SigmaStrValueManager()
