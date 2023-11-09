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

import re
from typing import Tuple, List, Dict, Optional

from app.converter.backends.splunk.const import splunk_query_details
from app.converter.backends.splunk.mapping import SplunkMappings, splunk_mappings
from app.converter.backends.splunk.siem_functions import SplunkFunctions
from app.converter.backends.splunk.tokenizer import SplunkTokenizer
from app.converter.core.models.functions.types import ParsedFunctions
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.parser import Parser
from app.converter.core.operator_types.output import SiemContainer, MetaInfoContainer


class SplunkParser(Parser):
    details: PlatformDetails = splunk_query_details
    siem_functions = SplunkFunctions()

    log_source_pattern = r"___source_type___\s*=\s*(?:\"(?P<d_q_value>[%a-zA-Z_*:0-9\-/]+)\"|(?P<value>[%a-zA-Z_*:0-9\-/]+))(?:\s+(?:and|or)\s+|\s+)?"
    log_source_key_types = ("index", "source", "sourcetype", "sourcecategory")

    mappings: SplunkMappings = splunk_mappings
    tokenizer = SplunkTokenizer()

    def _parse_log_sources(self, query: str) -> Tuple[Dict[str, List[str]], str]:
        log_sources = {}
        for source_type in self.log_source_key_types:
            log_sources.setdefault(source_type, [])
            pattern = self.log_source_pattern.replace('___source_type___', source_type)
            while search := re.search(pattern, query, flags=re.IGNORECASE):
                results = search.groupdict()
                value = results.get("value")
                log_sources.setdefault(source_type, []).append(value)
                pos_start = search.start()
                pos_end = search.end()
                query = query[:pos_start] + query[pos_end:]

        return log_sources, query

    def _parse_functions(self, query: str) -> Tuple[ParsedFunctions, str]:
        if search_result := re.search(r"\|(.+?)$", query):
            parsed_functions = self.siem_functions.parse(search_result.group().strip(" |"))
            pos_start = search_result.start()
            pos_end = search_result.end()
            query = query[:pos_start] + query[pos_end:]
            return parsed_functions, query.strip(" ")

        return ParsedFunctions(), query

    def _parse_query(self, query: str) -> Tuple[Dict[str, List[str]], ParsedFunctions, str]:
        query = query.strip()
        log_sources, query = self._parse_log_sources(query)
        functions, query = self._parse_functions(query)
        return log_sources, functions, query

    @staticmethod
    def _get_meta_info(source_mapping_ids: List[str], meta_info: Optional[dict]) -> MetaInfoContainer:
        return MetaInfoContainer(
            source_mapping_ids=source_mapping_ids
        )

    def parse(self, text: str) -> SiemContainer:
        log_sources, functions, query = self._parse_query(text)
        tokens, source_mappings = self.get_tokens_and_source_mappings(query, log_sources)

        return SiemContainer(
            query=tokens,
            meta_info=self._get_meta_info([source_mapping.source_id for source_mapping in source_mappings], {}),
            functions=functions
        )
