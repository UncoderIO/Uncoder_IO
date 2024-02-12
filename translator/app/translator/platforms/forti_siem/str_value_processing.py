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
    StrValue,
    StrValueManager,
    UnboundLenWildCard,
)
from app.translator.platforms.forti_siem.escape_manager import forti_siem_escape_manager

SPEC_SYMBOLS_MAP = {
    SingleSymbolWildCard: ".?",
    UnboundLenWildCard: ".*",
    ReStartOfStrSymbol: "^",
    ReEndOfStrSymbol: "$",
    ReWordSymbol: r"\w",
    ReDigitalSymbol: r"\d",
    ReWhiteSpaceSymbol: r"\s",
    ReAnySymbol: ".",
    ReZeroOrMoreQuantifier: "*",
    ReOneOrMoreQuantifier: "+",
    ReZeroOrOneQuantifier: "?",
}


class FortiSiemStrValueManager(StrValueManager):
    escape_manager = forti_siem_escape_manager

    def from_container_to_re_str(self, container: StrValue) -> str:
        result = ""
        for el in container.split_value:
            if isinstance(el, str):
                result += self.escape_manager.escape(el)
            elif isinstance(el, BaseSpecSymbol):
                if not (pattern := SPEC_SYMBOLS_MAP.get(type(el))):
                    raise NotImplementedError

                result += pattern

        return result


forti_siem_str_value_manager = FortiSiemStrValueManager()
