from typing import Optional, TypeVar, Union

from app.translator.core.escape_manager import EscapeManager


class BaseSpecSymbol:
    ...


SpecSymbolType = TypeVar("SpecSymbolType", bound=BaseSpecSymbol)


class SingleSymbolWildCard(BaseSpecSymbol):
    ...


class UnboundLenWildCard(BaseSpecSymbol):
    ...


class ReStartOfStrSymbol(BaseSpecSymbol):
    ...


class ReEndOfStrSymbol(BaseSpecSymbol):
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


class StrValueManager:
    escape_manager: EscapeManager = None

    @staticmethod
    def from_str_to_container(value: str) -> StrValue:
        return StrValue(value=value, split_value=[value])

    @staticmethod
    def from_re_str_to_container(value: str) -> StrValue:
        return StrValue(value=value, split_value=[value])

    @staticmethod
    def from_container_to_str(container: StrValue) -> str:
        return "".join(container.split_value)

    @staticmethod
    def from_container_to_re_str(container: StrValue) -> str:
        return "".join(container.split_value)
