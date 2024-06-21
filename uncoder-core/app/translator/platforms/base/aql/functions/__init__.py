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

import os.path
import re
from typing import Optional, Union

from app.translator.core.custom_types.functions import FunctionType
from app.translator.core.exceptions.functions import InvalidFunctionSignature, NotSupportedFunctionException
from app.translator.core.functions import PlatformFunctions
from app.translator.core.models.field import Field
from app.translator.core.models.functions.base import Function, ParsedFunctions
from app.translator.core.models.functions.sort import SortLimitFunction
from app.translator.platforms.base.aql.const import TABLE_PATTERN
from app.translator.platforms.base.aql.functions.const import (
    AGGREGATION_FUNCTIONS_MAP,
    AQLFunctionType,
    func_aliases_ctx_var,
)
from app.translator.platforms.base.aql.functions.manager import AQLFunctionsManager, aql_functions_manager


class AQLFunctions(PlatformFunctions):
    dir_path: str = os.path.abspath(os.path.dirname(__file__))

    function_delimiter = ""
    functions_pattern = r"\s(?P<function_name>(group by|order by|last))"
    manager: AQLFunctionsManager = aql_functions_manager

    def parse(self, query: str) -> tuple[str, ParsedFunctions]:
        parsed = []
        not_supported = []
        invalid = []

        query_prefix, query = re.split(TABLE_PATTERN, query, flags=re.IGNORECASE)
        if not re.match(r"\s*SELECT\s+(?:UTF8\(payload\)|\*)", query_prefix, flags=re.IGNORECASE):
            self._parse_function(
                function_name=AQLFunctionType.fields,
                function=query_prefix,
                parsed=parsed,
                not_supported=not_supported,
                invalid=invalid,
            )
        aliases = self._parse_aliases(parsed=parsed)
        self.__set_aliases_ctx_var(value=list(aliases.keys()))
        if search := re.search(self.functions_pattern, query, flags=re.IGNORECASE):
            agg_functions = query[search.start() :]
            query = query[: search.start()]
            self._parse_function(
                function_name=AQLFunctionType.aggregation_data_function,
                function=agg_functions,
                parsed=parsed,
                not_supported=not_supported,
                invalid=invalid,
            )

        if group_by_func := self.__filter_function_by_type(parsed, FunctionType.stats):
            if table_func := self.__filter_function_by_type(parsed, FunctionType.table):
                self.__group_by_post_processing(group_by_func, table_func)
            else:
                parsed = [func for func in parsed if func.name != FunctionType.stats]
                not_supported.append(group_by_func.raw)

        parsed = self.__merge_sort_limit_functions(parsed)
        self.__set_aliases_ctx_var(value=[])
        query = re.sub(r"[a-zA-Z0-9_\-\s]+WHERE", "", query, 1, flags=re.IGNORECASE)
        return query, ParsedFunctions(functions=parsed, not_supported=not_supported, invalid=invalid, aliases=aliases)

    @staticmethod
    def __set_aliases_ctx_var(value: list[str]) -> None:
        func_aliases_ctx_var.set(value)

    @staticmethod
    def __filter_function_by_type(functions: list[Function], function_type: str) -> Optional[Function]:
        for func in functions:
            if func.name == function_type:
                return func

    @staticmethod
    def __group_by_post_processing(group_by_func: Function, table_func: Function) -> None:
        agg_functions = []
        for index, arg in enumerate(table_func.args):
            if isinstance(arg, Function) and arg.name in AGGREGATION_FUNCTIONS_MAP.values():
                agg_functions.append(arg)
                table_func.args[index] = arg.alias

        group_by_func.args = agg_functions

    @staticmethod
    def __merge_sort_limit_functions(functions: list[Function]) -> list[Function]:
        indices = []
        funcs = []
        for index, func in enumerate(functions):
            if func.name == FunctionType.sort_limit:
                func: SortLimitFunction
                indices.append(index)
                funcs.append(func)

        if len(funcs) == 2:  # noqa: PLR2004
            funcs[1].args = funcs[1].args or funcs[0].args
            funcs[1].limit = funcs[1].limit or funcs[0].limit
            funcs[1].raw = f"{funcs[1].raw} {funcs[0].raw}"
            functions.pop(indices[0])

        return functions

    def _parse_function(
        self, function: str, function_name: str, parsed: list[Function], not_supported: list[str], invalid: list[str]
    ) -> None:
        try:
            function_parser = self.manager.get_hof_parser(function_name)
            function_token = function_parser.parse(func_body=function, raw=function)
            if isinstance(function_token, list):
                parsed.extend(function_token)
            else:
                parsed.append(function_token)
        except NotSupportedFunctionException:
            not_supported.append(function)
        except InvalidFunctionSignature:
            invalid.append(function)

    @staticmethod
    def _parse_aliases(parsed: list[Union[Field, Function]]) -> dict[str, Function]:
        return {
            arg.alias.name: arg
            for function in parsed
            for arg in function.args
            if isinstance(arg, Function) and arg.alias
        }


aql_functions = AQLFunctions()
