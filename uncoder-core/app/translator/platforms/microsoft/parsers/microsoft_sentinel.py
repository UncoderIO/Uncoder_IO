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
from app.translator.platforms.microsoft.const import microsoft_sentinel_query_details
from app.translator.platforms.microsoft.functions import MicrosoftFunctions, microsoft_sentinel_functions
from app.translator.platforms.microsoft.mapping import MicrosoftSentinelMappings, microsoft_sentinel_mappings
from app.translator.platforms.microsoft.tokenizer import MicrosoftSentinelTokenizer


@parser_manager.register_roota_parser
class MicrosoftSentinelQueryParser(PlatformQueryParser):
    platform_functions: MicrosoftFunctions = microsoft_sentinel_functions
    mappings: MicrosoftSentinelMappings = microsoft_sentinel_mappings
    tokenizer = MicrosoftSentinelTokenizer()
    details: PlatformDetails = microsoft_sentinel_query_details

    def _parse_query(self, query: str) -> tuple[str, dict[str, list[str]], ParsedFunctions]:
        table, query, functions = self.platform_functions.parse(query)
        log_sources = {"table": [table]}
        return query, log_sources, functions

    def parse(self, raw_query_container: RawQueryContainer) -> TokenizedQueryContainer:
        query, log_sources, functions = self._parse_query(query=raw_query_container.query)
        tokens, source_mappings = self.get_tokens_and_source_mappings(query, log_sources)
        self.set_functions_fields_generic_names(functions=functions, source_mappings=source_mappings)
        meta_info = raw_query_container.meta_info
        meta_info.source_mapping_ids = [source_mapping.source_id for source_mapping in source_mappings]
        return TokenizedQueryContainer(tokens=tokens, meta_info=meta_info, functions=functions)
