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

from app.translator.core.models.functions.base import ParsedFunctions
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import RawQueryContainer, TokenizedQueryContainer
from app.translator.core.parser import PlatformQueryParser
from app.translator.managers import parser_manager
from app.translator.platforms.logscale.const import logscale_query_details
from app.translator.platforms.logscale.functions import LogScaleFunctions, log_scale_functions
from app.translator.platforms.logscale.mapping import LogScaleMappings, logscale_query_mappings
from app.translator.platforms.logscale.tokenizer import LogScaleTokenizer


@parser_manager.register_supported_by_roota
class LogScaleQueryParser(PlatformQueryParser):
    details: PlatformDetails = logscale_query_details
    platform_functions: LogScaleFunctions = log_scale_functions
    tokenizer = LogScaleTokenizer()
    mappings: LogScaleMappings = logscale_query_mappings

    wrapped_with_comment_pattern = r"^\s*/\*(?:|\n|.)*\*/"

    def _parse_query(self, query: str) -> tuple[str, ParsedFunctions]:
        functions, query = self.platform_functions.parse(query)
        return query, functions

    def parse(self, raw_query_container: RawQueryContainer) -> TokenizedQueryContainer:
        query, functions = self._parse_query(query=raw_query_container.query)
        query_tokens = self.get_query_tokens(query)
        field_tokens = self.get_field_tokens(query_tokens, functions.functions)
        source_mappings = self.get_source_mappings(field_tokens, {})
        meta_info = raw_query_container.meta_info
        meta_info.query_fields = field_tokens
        meta_info.source_mapping_ids = [source_mapping.source_id for source_mapping in source_mappings]
        return TokenizedQueryContainer(tokens=query_tokens, meta_info=meta_info, functions=functions)
