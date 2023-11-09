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

from app.converter.backends.microsoft.const import microsoft_sentinel_query_details
from app.converter.backends.microsoft.siem_functions.base import MicroSoftQueryFunctions
from app.converter.backends.microsoft.mapping import MicrosoftSentinelMappings, microsoft_sentinel_mappings
from app.converter.backends.microsoft.tokenizer import MicrosoftSentinelTokenizer
from app.converter.core.models.functions.types import ParsedFunctions
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.parser import Parser
from app.converter.core.operator_types.output import SiemContainer, MetaInfoContainer


class MicrosoftParser(Parser):
    siem_functions = MicroSoftQueryFunctions()
    mappings: MicrosoftSentinelMappings = microsoft_sentinel_mappings
    tokenizer = MicrosoftSentinelTokenizer()
    details: PlatformDetails = microsoft_sentinel_query_details

    @staticmethod
    def _get_meta_info(source_mapping_ids: List[str], meta_info: dict) -> MetaInfoContainer:
        return MetaInfoContainer(source_mapping_ids=source_mapping_ids)

    def _parse_query(self, query: str) -> Tuple[str, Dict[str, List[str]], ParsedFunctions]:
        functions, split_query = self.siem_functions.parse(query)
        table, query = split_query[0], " and ".join(split_query[1:])
        log_sources = dict(table=[split_query[0]])
        return query, log_sources, functions

    def parse(self, text: str) -> SiemContainer:
        query, log_sources, functions = self._parse_query(query=text)
        tokens, source_mappings = self.get_tokens_and_source_mappings(query, log_sources)

        return SiemContainer(
            query=tokens,
            meta_info=self._get_meta_info([source_mapping.source_id for source_mapping in source_mappings], {}),
            functions=functions
        )
