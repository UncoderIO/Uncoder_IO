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
import re
from abc import ABC, abstractmethod
from typing import Union

from app.translator.core.exceptions.parser import TokenizerGeneralException
from app.translator.core.functions import PlatformFunctions
from app.translator.core.mapping import BasePlatformMappings, SourceMapping
from app.translator.core.models.field import FieldValue
from app.translator.core.models.functions.base import ParsedFunctions
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import RawQueryContainer, TokenizedQueryContainer
from app.translator.core.tokenizer import TOKEN_TYPE, QueryTokenizer


class QueryParser(ABC):
    wrapped_with_comment_pattern: str = None

    def remove_comments(self, text: str) -> str:
        return re.sub(self.wrapped_with_comment_pattern, "\n", text).strip()

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        return RawQueryContainer(query=text, language=language)

    @abstractmethod
    def parse(self, raw_query_container: RawQueryContainer) -> TokenizedQueryContainer:
        raise NotImplementedError("Abstract method")


class PlatformQueryParser(QueryParser, ABC):
    mappings: BasePlatformMappings = None
    tokenizer: QueryTokenizer = None
    details: PlatformDetails = None
    platform_functions: PlatformFunctions = None

    def get_tokens_and_source_mappings(
        self, query: str, log_sources: dict[str, Union[str, list[str]]]
    ) -> tuple[list[TOKEN_TYPE], list[SourceMapping]]:
        if not query:
            raise TokenizerGeneralException("Can't translate empty query. Please provide more details")
        tokens = self.tokenizer.tokenize(query=query)
        field_tokens = [token.field for token in self.tokenizer.filter_tokens(tokens, FieldValue)]
        field_names = [field.source_name for field in field_tokens]
        source_mappings = self.mappings.get_suitable_source_mappings(field_names=field_names, **log_sources)
        self.tokenizer.set_field_tokens_generic_names_map(field_tokens, source_mappings, self.mappings.default_mapping)

        return tokens, source_mappings

    def set_functions_fields_generic_names(
        self, functions: ParsedFunctions, source_mappings: list[SourceMapping]
    ) -> None:
        field_tokens = self.tokenizer.get_field_tokens_from_func_args(args=functions.functions)
        self.tokenizer.set_field_tokens_generic_names_map(field_tokens, source_mappings, self.mappings.default_mapping)
