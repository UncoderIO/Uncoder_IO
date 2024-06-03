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
from functools import cached_property
from typing import TYPE_CHECKING, Any, Optional

from app.translator.core.exceptions.functions import InvalidFunctionSignature, NotSupportedFunctionException
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.field import Field
from app.translator.core.models.functions.base import Function, ParsedFunctions, RenderedFunctions
from settings import INIT_FUNCTIONS

if TYPE_CHECKING:
    from app.translator.core.render import PlatformQueryRender


@dataclass
class FunctionMatchContainer:
    name: str
    match: re.Match


class BaseFunctionParser(ABC):
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
    @abstractmethod
    def render(self, function: Function, source_mapping: SourceMapping) -> str:
        raise NotImplementedError

    @staticmethod
    def concat_kwargs(kwargs: dict[str, str]) -> str:
        result = ""
        for key, value in kwargs.items():
            if value:
                result = f"{result}, {key}={value}" if result else f"{key}={value}"

        return result

    @staticmethod
    def map_field(field: Field, source_mapping: SourceMapping) -> str:
        generic_field_name = field.get_generic_field_name(source_mapping.source_id)
        mapped_field = source_mapping.fields_mapping.get_platform_field_name(generic_field_name=generic_field_name)
        if isinstance(mapped_field, list):
            mapped_field = mapped_field[0]

        return mapped_field if mapped_field else field.source_name


class PlatformFunctionsManager:
    def __init__(self):
        self._parsers_map: dict[str, HigherOrderFunctionParser] = {}
        self._renders_map: dict[str, FunctionRender] = {}
        self._in_query_renders_map: dict[str, FunctionRender] = {}
        self._names_map: dict[str, str] = {}
        self._order_to_render: dict[str, int] = {}
        self._render_to_prefix_functions: list[str] = []

    def post_init_configure(self, platform_render: PlatformQueryRender) -> None:
        raise NotImplementedError

    @cached_property
    def _inverted_names_map(self) -> dict[str, str]:
        return {value: key for key, value in self._names_map.items()}

    def get_parser(self, generic_func_name: str) -> HigherOrderFunctionParser:
        if INIT_FUNCTIONS and (parser := self._parsers_map.get(generic_func_name)):
            return parser

        raise NotSupportedFunctionException

    def get_render(self, generic_func_name: str) -> FunctionRender:
        if INIT_FUNCTIONS and (render := self._renders_map.get(generic_func_name)):
            return render

        raise NotSupportedFunctionException

    def get_in_query_render(self, generic_func_name: str) -> FunctionRender:
        if INIT_FUNCTIONS and (render := self._in_query_renders_map.get(generic_func_name)):
            return render

        raise NotSupportedFunctionException

    def get_generic_func_name(self, platform_func_name: str) -> Optional[str]:
        if INIT_FUNCTIONS and (generic_func_name := self._names_map.get(platform_func_name)):
            return generic_func_name

        raise NotSupportedFunctionException

    def get_platform_func_name(self, generic_func_name: str) -> Optional[str]:
        if INIT_FUNCTIONS:
            return self._inverted_names_map.get(generic_func_name)

    @property
    def order_to_render(self) -> dict[str, int]:
        if INIT_FUNCTIONS:
            return self._order_to_render

        return {}

    @property
    def render_to_prefix_functions(self) -> list[str]:
        if INIT_FUNCTIONS:
            return self._render_to_prefix_functions

        return []


class PlatformFunctions:
    manager: PlatformFunctionsManager = PlatformFunctionsManager()
    function_delimiter = "|"

    def parse(self, query: str) -> ParsedFunctions:
        parsed = []
        not_supported = []
        invalid = []
        functions = query.split(self.function_delimiter)
        for func in functions:
            split_func = func.strip().split(" ")
            func_name, func_body = split_func[0], " ".join(split_func[1:])
            try:
                func_parser = self.manager.get_parser(self.manager.get_generic_func_name(func_name))
                parsed.append(func_parser.parse(func_body, func))
            except NotSupportedFunctionException:
                not_supported.append(func)
            except InvalidFunctionSignature:
                invalid.append(func)

        return ParsedFunctions(
            functions=parsed,
            not_supported=[self.wrap_function_with_delimiter(func) for func in not_supported],
            invalid=invalid,
        )

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
                if func.name in self.manager.render_to_prefix_functions:
                    rendered_prefix += _rendered
                else:
                    rendered += self.wrap_function_with_delimiter(_rendered)
            except NotSupportedFunctionException:
                not_supported.append(func.raw)

        not_supported = [self.wrap_function_with_delimiter(func.strip()) for func in not_supported]
        return RenderedFunctions(rendered_prefix=rendered_prefix, rendered=rendered, not_supported=not_supported)

    def wrap_function_with_delimiter(self, func: str) -> str:
        return f" {self.function_delimiter} {func}"
