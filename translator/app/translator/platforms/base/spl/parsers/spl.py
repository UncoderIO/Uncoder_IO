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

from app.translator.core.models.functions.base import ParsedFunctions
from app.translator.core.models.query_container import RawQueryContainer, TokenizedQueryContainer
from app.translator.core.parser import PlatformQueryParser
from app.translator.platforms.base.spl.tokenizer import SplTokenizer


class SplQueryParser(PlatformQueryParser):
    log_source_pattern = r"^___source_type___\s*=\s*(?:\"(?P<d_q_value>[%a-zA-Z_*:0-9\-/]+)\"|(?P<value>[%a-zA-Z_*:0-9\-/]+))(?:\s+(?:and|or)\s+|\s+)?"  # noqa: E501
    log_source_key_types = ("index", "source", "sourcetype", "sourcecategory")

    tokenizer = SplTokenizer()

    def _parse_log_sources(self, query: str) -> tuple[dict[str, list[str]], str]:
        log_sources = {}
        for source_type in self.log_source_key_types:
            log_sources.setdefault(source_type, [])
            pattern = self.log_source_pattern.replace("___source_type___", source_type)
            while search := re.search(pattern, query, flags=re.IGNORECASE):
                group_dict = search.groupdict()
                value = group_dict.get("d_q_value") or group_dict.get("value")
                log_sources.setdefault(source_type, []).append(value)
                pos_start = search.start()
                pos_end = search.end()
                query = query[:pos_start] + query[pos_end:]
                query = query.replace("()", "")

        return log_sources, query

    def _parse_query(self, query: str) -> tuple[str, dict[str, list[str]], ParsedFunctions]:
        query = query.strip()
        log_sources, query = self._parse_log_sources(query)
        query, functions = self.platform_functions.parse(query)
        return query, log_sources, functions

    def parse(self, raw_query_container: RawQueryContainer) -> TokenizedQueryContainer:
        query, log_sources, functions = self._parse_query(raw_query_container.query)
        tokens, source_mappings = self.get_tokens_and_source_mappings(query, log_sources)
        self.set_functions_fields_generic_names(functions=functions, source_mappings=source_mappings)
        meta_info = raw_query_container.meta_info
        meta_info.source_mapping_ids = [source_mapping.source_id for source_mapping in source_mappings]
        return TokenizedQueryContainer(tokens=tokens, meta_info=meta_info, functions=functions)
