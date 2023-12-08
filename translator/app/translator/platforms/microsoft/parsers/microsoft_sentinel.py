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

from typing import Tuple, List, Dict

from app.translator.core.models.functions.base import ParsedFunctions
from app.translator.platforms.microsoft.const import microsoft_sentinel_query_details
from app.translator.platforms.microsoft.functions import MicrosoftFunctions, microsoft_sentinel_functions
from app.translator.platforms.microsoft.mapping import MicrosoftSentinelMappings, microsoft_sentinel_mappings
from app.translator.platforms.microsoft.tokenizer import MicrosoftSentinelTokenizer
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.parser import Parser
from app.translator.core.models.parser_output import SiemContainer, MetaInfoContainer


class MicrosoftParser(Parser):
    platform_functions: MicrosoftFunctions = microsoft_sentinel_functions
    mappings: MicrosoftSentinelMappings = microsoft_sentinel_mappings
    tokenizer = MicrosoftSentinelTokenizer()
    details: PlatformDetails = microsoft_sentinel_query_details

    @staticmethod
    def _get_meta_info(source_mapping_ids: List[str], meta_info: dict) -> MetaInfoContainer:
        return MetaInfoContainer(source_mapping_ids=source_mapping_ids)

    def _parse_query(self, query: str) -> Tuple[str, Dict[str, List[str]], ParsedFunctions]:
        table, query, functions = self.platform_functions.parse(query)
        log_sources = dict(table=[table])
        return query, log_sources, functions

    def parse(self, text: str) -> SiemContainer:
        query, log_sources, functions = self._parse_query(query=text)
        tokens, source_mappings = self.get_tokens_and_source_mappings(query, log_sources)
        self.set_functions_fields_generic_names(functions=functions, source_mappings=source_mappings)
        return SiemContainer(
            query=tokens,
            meta_info=self._get_meta_info([source_mapping.source_id for source_mapping in source_mappings], {}),
            functions=functions
        )
