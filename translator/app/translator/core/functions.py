"""
Uncoder IO Commercial Edition License
-----------------------------------------------------------------
Copyright (c) 2023 SOC Prime, Inc.

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

from abc import ABC, abstractmethod
from functools import cached_property
from typing import Dict, List, TYPE_CHECKING, Optional

from app.translator.core.exceptions.functions import NotSupportedFunctionException, InvalidFunctionSignature
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.field import Field
from app.translator.core.models.functions.base import Function, ParsedFunctions
from app.translator.core.tokenizer import BaseTokenizer
from settings import INIT_FUNCTIONS

if TYPE_CHECKING:
    from app.translator.core.render import BaseQueryRender


class FunctionParser(ABC):
    tokenizer: BaseTokenizer = None

    @abstractmethod
    def parse(self, func_body: str) -> Function:
        raise NotImplementedError()


class FunctionRender(ABC):

    @abstractmethod
    def render(self, function: Function, source_mapping: SourceMapping) -> str:
        raise NotImplementedError()

    @staticmethod
    def concat_kwargs(kwargs: Dict[str, str]) -> str:
        result = ""
        for key, value in kwargs.items():
            if value:
                result = f"{result}, {key}={value}" if result else f"{key}={value}"

        return result

    @staticmethod
    def map_field(field: Field, source_mapping: SourceMapping) -> str:
        generic_field_name = field.generic_names_map[source_mapping.source_id]
        mapped_field = source_mapping.fields_mapping.get_platform_field_name(generic_field_name=generic_field_name)
        if isinstance(mapped_field, list):
            mapped_field = mapped_field[0]

        return mapped_field if mapped_field else field.source_name


class PlatformFunctionsManager(ABC):
    _parsers_map: Dict[str, FunctionParser] = {}
    _renders_map: Dict[str, FunctionRender] = {}
    _names_map: Dict[str, str] = {}

    @abstractmethod
    def init_search_func_render(self, platform_render: BaseQueryRender) -> None:
        raise NotImplementedError()

    @cached_property
    def _inverted_names_map(self) -> Dict[str, str]:
        return {value: key for key, value in self._names_map.items()}

    def get_parser(self, func_name: str) -> Optional[FunctionParser]:
        if INIT_FUNCTIONS:
            return self._parsers_map.get(func_name)

    def get_render(self, func_name: str) -> Optional[FunctionRender]:
        if INIT_FUNCTIONS:
            return self._renders_map.get(func_name)

    def get_generic_func_name(self, platform_func_name: str) -> Optional[str]:
        if INIT_FUNCTIONS:
            return self._names_map.get(platform_func_name)

    def get_platform_func_name(self, generic_func_name: str) -> Optional[str]:
        if INIT_FUNCTIONS:
            return self._inverted_names_map.get(generic_func_name)


class PlatformFunctions:
    manager: PlatformFunctionsManager = None
    function_delimiter = "|"

    def parse(self, query: str) -> ParsedFunctions:
        parsed = []
        not_supported = []
        invalid = []
        functions = query.split(self.function_delimiter)
        for func in functions:
            split_func = func.strip().split(' ')
            func_name, func_body = split_func[0], " ".join(split_func[1:])
            if func_parser := self.manager.get_parser(self.manager.get_generic_func_name(func_name)):
                try:
                    parsed.append(func_parser.parse(func_body))
                except NotSupportedFunctionException:
                    not_supported.append(func)
                except InvalidFunctionSignature:
                    invalid.append(func)
            else:
                not_supported.append(func)
        return ParsedFunctions(
            functions=parsed,
            not_supported=[self.wrap_function_with_delimiter(func) for func in not_supported],
            invalid=invalid
        )

    def render(self, functions: List[Function], source_mapping: SourceMapping) -> str:
        result = ""
        for func in functions:
            if not (func_render := self.manager.get_render(func.name)):
                raise NotImplementedError()

            func_str = self.wrap_function_with_delimiter(func_render.render(func, source_mapping))
            result = f"{result} {func_str}" if result else func_str

        return result

    def wrap_function_with_delimiter(self, func: str) -> str:
        return f" {self.function_delimiter} {func}"
