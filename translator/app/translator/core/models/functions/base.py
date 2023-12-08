from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Union

from app.translator.core.models.field import Field, Keyword
from app.translator.core.models.identifier import Identifier


@dataclass
class Function:
    name: str = None
    args: List[Union[Field, Keyword, Function, Identifier]] = field(default_factory=list)
    as_clause: str = None
    by_clauses: List[Field] = field(default_factory=list)


@dataclass
class ParsedFunctions:
    functions: List[Function] = field(default_factory=list)
    not_supported: List[str] = field(default_factory=list)
    invalid: List[str] = field(default_factory=list)
