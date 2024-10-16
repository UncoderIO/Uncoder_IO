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

from app.translator.core.models.query_container import RawQueryContainer, TokenizedQueryContainer
from app.translator.core.parser import PlatformQueryParser
from app.translator.platforms.base.sql.tokenizer import SqlTokenizer


class SqlQueryParser(PlatformQueryParser):
    tokenizer = SqlTokenizer()
    query_delimiter_pattern = r"\sFROM\s\S*\sWHERE\s"
    table_pattern = r"\sFROM\s(?P<table>[a-zA-Z\.\-\*]+)\sWHERE\s"

    wrapped_with_comment_pattern = r"^\s*--.*(?:\n|$)"

    def _parse_query(self, query: str) -> tuple[str, dict[str, list[str]]]:
        log_source = {"table": []}
        if re.search(self.query_delimiter_pattern, query, flags=re.IGNORECASE):
            table_search = re.search(self.table_pattern, query)
            table = table_search.group("table")
            log_source["table"] = [table]
            return re.split(self.query_delimiter_pattern, query, flags=re.IGNORECASE)[1], log_source

        return query, log_source

    def parse(self, raw_query_container: RawQueryContainer) -> TokenizedQueryContainer:
        query, log_sources = self._parse_query(raw_query_container.query)
        query_tokens = self.get_query_tokens(query)
        field_tokens = self.get_field_tokens(query_tokens)
        source_mappings = self.get_source_mappings(field_tokens, log_sources)
        meta_info = raw_query_container.meta_info
        meta_info.query_fields = field_tokens
        meta_info.source_mapping_ids = [source_mapping.source_id for source_mapping in source_mappings]
        return TokenizedQueryContainer(tokens=query_tokens, meta_info=meta_info)
