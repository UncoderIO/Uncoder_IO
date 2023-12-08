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

from typing import List

from app.translator.platforms.chronicle.const import chronicle_query_details
from app.translator.platforms.chronicle.mapping import chronicle_mappings, ChronicleMappings
from app.translator.platforms.chronicle.tokenizer import ChronicleQueryTokenizer
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.parser import Parser
from app.translator.core.models.parser_output import SiemContainer, MetaInfoContainer


class ChronicleParser(Parser):
    mappings: ChronicleMappings = chronicle_mappings
    tokenizer: ChronicleQueryTokenizer = ChronicleQueryTokenizer()
    details: PlatformDetails = chronicle_query_details

    def _get_meta_info(self, source_mapping_ids: List[str]) -> MetaInfoContainer:
        return MetaInfoContainer(source_mapping_ids=source_mapping_ids)

    def parse(self, text: str) -> SiemContainer:
        tokens, source_mappings = self.get_tokens_and_source_mappings(text, {})
        return SiemContainer(
            query=tokens,
            meta_info=self._get_meta_info([source_mapping.source_id for source_mapping in source_mappings])
        )
