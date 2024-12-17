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

from typing import ClassVar, Optional, TypeVar, Union

from app.translator.core.custom_types.values import ValueType
from app.translator.core.escape_manager import EscapeManager


class BaseSpecSymbol:
    ...


SpecSymbolType = TypeVar("SpecSymbolType", bound=BaseSpecSymbol)


class SingleSymbolWildCard(BaseSpecSymbol):
    ...


class UnboundLenWildCard(BaseSpecSymbol):
    ...


class ReEndOfStrSymbol(BaseSpecSymbol):
    ...


class ReWordBoundarySymbol(BaseSpecSymbol):
    ...


class ReWordSymbol(BaseSpecSymbol):
    ...


class ReDigitalSymbol(BaseSpecSymbol):
    ...


class ReAnySymbol(BaseSpecSymbol):
    ...


class ReWhiteSpaceSymbol(BaseSpecSymbol):
    ...


class ReOneOrMoreQuantifier(BaseSpecSymbol):
    ...


class ReZeroOrMoreQuantifier(BaseSpecSymbol):
    ...


class ReZeroOrOneQuantifier(BaseSpecSymbol):
    ...


class ReLeftParenthesis(BaseSpecSymbol):
    ...


class ReRightParenthesis(BaseSpecSymbol):
    ...


class ReLeftSquareBracket(BaseSpecSymbol):
    ...


class ReRightSquareBracket(BaseSpecSymbol):
    ...


class ReLeftCurlyBracket(BaseSpecSymbol):
    ...


class ReRightCurlyBracket(BaseSpecSymbol):
    ...


class ReOrOperator(BaseSpecSymbol):
    ...


class ReCaretSymbol(BaseSpecSymbol):
    ...


class ReCommaSymbol(BaseSpecSymbol):
    ...


class ReHyphenSymbol(BaseSpecSymbol):
    ...


class StrValue(str):
    def __new__(cls, value: str, split_value: Optional[list[Union[str, SpecSymbolType]]] = None):  # noqa: ARG003
        return super().__new__(cls, value)

    def __init__(
        self,
        value: str,  # noqa: ARG002
        split_value: Optional[list[Union[str, SpecSymbolType]]] = None,
    ) -> None:
        self.split_value = split_value or []

    @property
    def has_spec_symbols(self) -> bool:
        return any(isinstance(el, BaseSpecSymbol) for el in self.split_value)


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


CONTAINER_SPEC_SYMBOLS_MAP = {
    SingleSymbolWildCard: "?",
    UnboundLenWildCard: "*",
    ReAnySymbol: ".",
    ReWordBoundarySymbol: r"\b",
    ReWordSymbol: r"\w",
    ReDigitalSymbol: r"\d",
    ReWhiteSpaceSymbol: r"\s",
    ReZeroOrMoreQuantifier: "*",
    ReOneOrMoreQuantifier: "+",
    ReZeroOrOneQuantifier: "?",
    ReLeftSquareBracket: "[",
    ReRightSquareBracket: "]",
    ReLeftParenthesis: "(",
    ReRightParenthesis: ")",
    ReLeftCurlyBracket: "{",
    ReRightCurlyBracket: "}",
    ReOrOperator: "|",
    ReCaretSymbol: "^",
    ReEndOfStrSymbol: "$",
    ReCommaSymbol: ",",
    ReHyphenSymbol: "-",
}


class StrValueManager:
    escape_manager: EscapeManager = None
    str_spec_symbols_map: ClassVar[dict[str, type[BaseSpecSymbol]]] = {}
    re_str_alpha_num_symbols_map: ClassVar[dict[str, type[BaseSpecSymbol]]] = {}
    re_str_spec_symbols_map: ClassVar[dict[str, type[BaseSpecSymbol]]] = {}
    container_spec_symbols_map: ClassVar[dict[type[BaseSpecSymbol], str]] = CONTAINER_SPEC_SYMBOLS_MAP

    @staticmethod
    def from_str_to_container(
        value: str,
        value_type: str = ValueType.value,  # noqa: ARG004
        escape_symbol: Optional[str] = None,  # noqa: ARG004
    ) -> StrValue:
        return StrValue(value=value, split_value=[value])

    def from_re_str_to_container(self, value: str) -> StrValue:
        split = []
        prev_char = None
        inside_curly_brackets = False
        inside_square_brackets = False
        for char in value:
            if prev_char == "\\":
                if char == "\\":
                    split.append(char)
                    prev_char = None
                    continue
                if char in self.re_str_alpha_num_symbols_map:
                    split.append(self.re_str_alpha_num_symbols_map[char]())
                else:
                    split.append(char)
            elif char in self.re_str_spec_symbols_map:
                if char == "{":
                    inside_curly_brackets = True
                elif char == "}":
                    inside_curly_brackets = False
                elif char == "[":
                    inside_square_brackets = True
                elif char == "]":
                    inside_square_brackets = False
                elif (
                    char == ","
                    and not inside_curly_brackets
                    or char == "-"
                    and (not inside_square_brackets or isinstance(split[-1], ReLeftSquareBracket))
                ):
                    split.append(char)
                    continue
                split.append(self.re_str_spec_symbols_map[char]())
            elif char != "\\":
                split.append(char)

            prev_char = char

        return StrValue(value, self._concat(split))

    def from_container_to_str(self, container: StrValue, value_type: str = ValueType.value) -> str:
        result = ""
        for el in container.split_value:
            if isinstance(el, str):
                result += self.escape_manager.escape(el, value_type)
            elif isinstance(el, BaseSpecSymbol) and (pattern := self.container_spec_symbols_map.get(type(el))):
                result += pattern

        return result

    @staticmethod
    def _concat(split: list[Union[str, SpecSymbolType]]) -> list[Union[str, SpecSymbolType]]:
        result = []
        sub_str = ""
        for el in split:
            if isinstance(el, str):
                sub_str += el
            elif isinstance(el, BaseSpecSymbol):
                if sub_str:
                    result.append(sub_str)
                result.append(el)
                sub_str = ""

        if sub_str:
            result.append(sub_str)

        return result
