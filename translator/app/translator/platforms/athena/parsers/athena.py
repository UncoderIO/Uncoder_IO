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
from typing import Optional

from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import RawQueryContainer, TokenizedQueryContainer
from app.translator.core.parser import PlatformQueryParser
from app.translator.platforms.athena.const import athena_details
from app.translator.platforms.athena.mapping import AthenaMappings, athena_mappings
from app.translator.platforms.athena.tokenizer import AthenaTokenizer


class AthenaQueryParser(PlatformQueryParser):
    details: PlatformDetails = athena_details
    mappings: AthenaMappings = athena_mappings
    tokenizer = AthenaTokenizer()
    query_delimiter_pattern = r"\sFROM\s\S*\sWHERE\s"
    table_pattern = r"\sFROM\s(?P<table>[a-zA-Z\.\-\*]+)\sWHERE\s"

    def _parse_query(self, query: str) -> tuple[str, dict[str, Optional[str]]]:
        log_source = {"table": None}
        if re.search(self.query_delimiter_pattern, query, flags=re.IGNORECASE):
            table_search = re.search(self.table_pattern, query)
            table = table_search.group("table")
            log_source["table"] = table
            return re.split(self.query_delimiter_pattern, query, flags=re.IGNORECASE)[1], log_source

        return query, log_source

    def parse(self, raw_query_container: RawQueryContainer) -> TokenizedQueryContainer:
        query, log_sources = self._parse_query(raw_query_container.query)
        tokens, source_mappings = self.get_tokens_and_source_mappings(query, log_sources)
        meta_info = raw_query_container.meta_info
        meta_info.source_mapping_ids = [source_mapping.source_id for source_mapping in source_mappings]
        return TokenizedQueryContainer(tokens=tokens, meta_info=meta_info)
