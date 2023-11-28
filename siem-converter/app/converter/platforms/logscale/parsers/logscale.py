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

from typing import Tuple, List

from app.converter.platforms.logscale.const import logscale_query_details
from app.converter.platforms.logscale.mapping import logscale_mappings, LogScaleMappings
from app.converter.platforms.logscale.siem_functions import LogScaleQueryFunctions
from app.converter.core.models.functions.types import ParsedFunctions
from app.converter.platforms.logscale.tokenizer import LogScaleTokenizer
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.parser import Parser
from app.converter.core.models.parser_output import SiemContainer, MetaInfoContainer


class LogScaleParser(Parser):
    details: PlatformDetails = logscale_query_details
    siem_functions = LogScaleQueryFunctions()
    tokenizer = LogScaleTokenizer()
    mappings: LogScaleMappings = logscale_mappings

    @staticmethod
    def _get_meta_info(source_mapping_ids: List[str], metainfo: dict) -> MetaInfoContainer:
        return MetaInfoContainer(source_mapping_ids=source_mapping_ids)

    def _parse_query(self, query: str) -> Tuple[str, ParsedFunctions]:
        functions, splited_query = self.siem_functions.parse(query)
        return " and ".join(splited_query), functions

    def parse(self, text: str) -> SiemContainer:
        query, functions = self._parse_query(query=text)
        tokens, source_mappings = self.get_tokens_and_source_mappings(text, {})
        return SiemContainer(
            query=tokens,
            meta_info=self._get_meta_info([source_mapping.source_id for source_mapping in source_mappings], {}),
            functions=functions
        )
