from typing import Union

from app.translator.core.str_value_processing import (
    BaseSpecSymbol,
    ReAnySymbol,
    ReDigitalSymbol,
    ReEndOfStrSymbol,
    ReOneOrMoreQuantifier,
    ReStartOfStrSymbol,
    ReWhiteSpaceSymbol,
    ReWordSymbol,
    ReZeroOrMoreQuantifier,
    ReZeroOrOneQuantifier,
    SingleSymbolWildCard,
    SpecSymbolType,
    StrValue,
    StrValueManager,
    UnboundLenWildCard,
)

STR_SPEC_SYMBOLS = {
    "?": SingleSymbolWildCard,
    "*": UnboundLenWildCard,
}


RE_STR_SPEC_SYMBOLS_MAP = {
    "?": ReZeroOrOneQuantifier,
    "*": ReZeroOrMoreQuantifier,
    "+": ReOneOrMoreQuantifier,
    "^": ReStartOfStrSymbol,
    "$": ReEndOfStrSymbol,
    "w": ReWordSymbol,
    "d": ReDigitalSymbol,
    "s": ReWhiteSpaceSymbol,
    ".": ReAnySymbol,
}


class SigmaStrValueManager(StrValueManager):
    @staticmethod
    def __concat(split: list[Union[str, SpecSymbolType]]) -> list[Union[str, SpecSymbolType]]:
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

    def from_str_to_container(self, value: str) -> StrValue:
        split = []
        prev_char = None
        for char in value:
            if char == "\\":
                if prev_char == "\\":
                    split.append(char)
                    prev_char = None
                    continue
            elif char in ("?", "*"):
                if prev_char == "\\":
                    split.append(char)
                else:
                    split.append(STR_SPEC_SYMBOLS[char]())
            else:
                if prev_char == "\\":
                    split.append(prev_char)
                split.append(char)

            prev_char = char

        return StrValue(value, self.__concat(split))

    def from_re_str_to_container(self, value: str) -> StrValue:
        split = []
        prev_char = None
        for char in value:
            if prev_char == "\\":
                if char in ("d", "s", "w"):
                    split.append(RE_STR_SPEC_SYMBOLS_MAP[char]())
                elif char == "\\":
                    split.append(char)
                    prev_char = None
                    continue
                else:
                    split.append(char)
            else:
                if char in ("*", "?", "+", "^", "$", "."):
                    split.append(RE_STR_SPEC_SYMBOLS_MAP[char]())
                elif char != "\\":
                    split.append(char)

            prev_char = char

        return StrValue(value, self.__concat(split))


sigma_str_value_manager = SigmaStrValueManager()
