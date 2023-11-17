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
from typing import List, Tuple, Dict, Optional

from app.converter.platforms.athena.const import athena_details
from app.converter.platforms.athena.mapping import athena_mappings, AthenaMappings
from app.converter.platforms.athena.tokenizer import AthenaTokenizer
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.parser import Parser
from app.converter.core.operator_types.output import SiemContainer, MetaInfoContainer


class AthenaParser(Parser):
    details: PlatformDetails = athena_details
    mappings: AthenaMappings = athena_mappings
    tokenizer = AthenaTokenizer()
    query_delimiter_pattern = r"\sFROM\s\S*\sWHERE\s"
    table_pattern = r"\sFROM\s(?P<table>[a-zA-Z\.\-\*]+)\sWHERE\s"

    @staticmethod
    def _get_meta_info(source_mapping_ids: List[str]) -> MetaInfoContainer:
        return MetaInfoContainer(source_mapping_ids=source_mapping_ids)

    def _parse_query(self, text: str) -> Tuple[str, Dict[str, Optional[str]]]:
        log_source = {"table": None}
        if re.search(self.query_delimiter_pattern, text, flags=re.IGNORECASE):
            table_search = re.search(self.table_pattern, text)
            table = table_search.group("table")
            log_source["table"] = table
            return re.split(self.query_delimiter_pattern, text, flags=re.IGNORECASE)[1], log_source

        return text, log_source

    def parse(self, text: str) -> SiemContainer:
        query, log_sources = self._parse_query(text)
        tokens, source_mappings = self.get_tokens_and_source_mappings(query, log_sources)
        return SiemContainer(
            query=tokens,
            meta_info=self._get_meta_info([source_mapping.source_id for source_mapping in source_mappings]),
        )
