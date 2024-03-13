from dataclasses import dataclass


@dataclass
class EscapeDetails:
    pattern: str = None
    escape_symbols: str = "\\\\\g<1>"
