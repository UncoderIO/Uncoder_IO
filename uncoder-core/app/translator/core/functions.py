"""
Uncoder IO Commercial Edition License
-----------------------------------------------------------------
Copyright (c) 2024 SOC Prime, Inc.

This file is part of the Uncoder IO Commercial Edition ("CE") and is
licensed under the Uncoder IO Non-Commercial License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://github.com/UncoderIO/UncoderIO/blob/main/LICENSE

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-----------------------------------------------------------------
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union

from app.translator.core.exceptions.functions import NotSupportedFunctionException
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.functions.base import Function, ParsedFunctions, RenderedFunctions
from app.translator.core.models.query_tokens.field import Alias, Field, PredefinedField
from app.translator.tools.utils import execute_module
from settings import INIT_FUNCTIONS

if TYPE_CHECKING:
    from app.translator.core.render import PlatformQueryRender


@dataclass
class FunctionMatchContainer:
    name: str
    match: re.Match


class BaseFunctionParser(ABC):
    function_names_map: ClassVar[dict[str, str]] = {}
    functions_group_name: str = None
    manager: PlatformFunctionsManager = None

    def set_functions_manager(self, manager: PlatformFunctionsManager) -> BaseFunctionParser:
        self.manager = manager
        return self

    @abstractmethod
    def parse(self, *args, **kwargs) -> Function:
        raise NotImplementedError

    def tokenize_body(self, func_body: str) -> list[Any]:
        tokenized = []
        while func_body:
            identifier, func_body = self._get_next_token(func_body=func_body)
            tokenized.append(identifier)
        return tokenized

    def _get_next_token(self, func_body: str) -> tuple[Any, str]:
        raise NotImplementedError


class FunctionParser(BaseFunctionParser):
    @abstractmethod
    def parse(self, func_name: str, match: re.Match) -> Function:
        raise NotImplementedError

    @abstractmethod
    def get_func_match(self, higher_order_func_body: str) -> Optional[FunctionMatchContainer]:
        raise NotImplementedError


class HigherOrderFunctionParser(BaseFunctionParser):  # for highest level functions e.g. | stats, | search, | sort, etc.
    @abstractmethod
    def parse(self, func_body: str, raw: str) -> Function:
        raise NotImplementedError


class FunctionRender(ABC):
    function_names_map: ClassVar[dict[str, str]] = {}
    order_to_render: int = 0
    render_to_prefix: bool = False
    manager: PlatformFunctionsManager = None

    def set_functions_manager(self, manager: PlatformFunctionsManager) -> FunctionRender:
        self.manager = manager
        return self

    @abstractmethod
    def render(self, function: Function, source_mapping: SourceMapping) -> str:
        raise NotImplementedError

    def map_field(self, field: Union[Alias, Field], source_mapping: SourceMapping) -> str:
        if isinstance(field, Alias):
            return field.name

        if isinstance(field, Field):
            mappings = self.manager.platform_functions.platform_query_render.mappings
            mapped_fields = mappings.map_field(field, source_mapping)
            return mapped_fields[0]

        if isinstance(field, PredefinedField):
            return self.manager.platform_functions.platform_query_render.map_predefined_field(field)

        raise NotSupportedFunctionException


class PlatformFunctionsManager:
    platform_functions: PlatformFunctions = None

    def __init__(self):
        # {platform_func_name: HigherOrderFunctionParser}
        self._hof_parsers_map: dict[str, HigherOrderFunctionParser] = {}
        self._parsers_map: dict[str, FunctionParser] = {}  # {platform_func_name: FunctionParser}

        self._renders_map: dict[str, FunctionRender] = {}  # {generic_func_name: FunctionRender}
        self._order_to_render: dict[str, int] = {}  # {generic_func_name: int}

    def register_render(self, render_class: type[FunctionRender]) -> type[FunctionRender]:
        render = render_class()
        render.manager = self
        for generic_function_name in render.function_names_map:
            self._renders_map[generic_function_name] = render
            self._order_to_render[generic_function_name] = render.order_to_render

        return render_class

    def register_parser(self, parser_class: type[BaseFunctionParser]) -> type[BaseFunctionParser]:
        parser = parser_class()
        parser.manager = self
        parsers_map = self._hof_parsers_map if isinstance(parser, HigherOrderFunctionParser) else self._parsers_map
        for platform_function_name in parser.function_names_map:
            parsers_map[platform_function_name] = parser

        if parser.functions_group_name:
            parsers_map[parser.functions_group_name] = parser

        return parser_class

    def get_hof_parser(self, platform_func_name: str) -> HigherOrderFunctionParser:
        if INIT_FUNCTIONS and (parser := self._hof_parsers_map.get(platform_func_name)):
            return parser

        raise NotSupportedFunctionException

    def get_parser(self, platform_func_name: str) -> Optional[FunctionParser]:
        if INIT_FUNCTIONS and (parser := self._parsers_map.get(platform_func_name)):
            return parser

    def get_render(self, generic_func_name: str) -> FunctionRender:
        if INIT_FUNCTIONS and (render := self._renders_map.get(generic_func_name)):
            return render

        raise NotSupportedFunctionException

    @property
    def order_to_render(self) -> dict[str, int]:
        if INIT_FUNCTIONS:
            return self._order_to_render

        return {}


class PlatformFunctions:
    dir_path: str = None
    platform_query_render: PlatformQueryRender = None
    manager: PlatformFunctionsManager = PlatformFunctionsManager()

    function_delimiter = "|"

    def __init__(self):
        self.manager.platform_functions = self
        if self.dir_path:
            execute_module(f"{self.dir_path}/parsers/__init__.py")
            execute_module(f"{self.dir_path}/renders/__init__.py")

    def parse(self, query: str) -> ParsedFunctions:  # noqa: ARG002
        return ParsedFunctions()

    def _sort_functions_to_render(self, functions: list[Function]) -> list[Function]:
        return sorted(functions, key=lambda func: self.manager.order_to_render.get(func.name, 0))

    def render(self, functions: list[Function], source_mapping: SourceMapping) -> RenderedFunctions:
        rendered = ""
        rendered_prefix = ""
        not_supported = []
        functions = self._sort_functions_to_render(functions)
        for func in functions:
            try:
                func_render = self.manager.get_render(func.name)
                _rendered = func_render.render(func, source_mapping)
                if func_render.render_to_prefix:
                    rendered_prefix += _rendered
                else:
                    rendered += self.wrap_function_with_delimiter(_rendered)
            except NotSupportedFunctionException:
                not_supported.append(func.raw)

        not_supported = [self.wrap_function_with_delimiter(func.strip()) for func in not_supported]
        return RenderedFunctions(rendered_prefix=rendered_prefix, rendered=rendered, not_supported=not_supported)

    def wrap_function_with_delimiter(self, func: str) -> str:
        return f" {self.function_delimiter} {func}"
