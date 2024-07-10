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

from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import RawQueryContainer, TokenizedQueryContainer
from app.translator.core.parser import PlatformQueryParser
from app.translator.managers import parser_manager
from app.translator.platforms.chronicle.const import chronicle_query_details
from app.translator.platforms.chronicle.mapping import ChronicleMappings, chronicle_query_mappings
from app.translator.platforms.chronicle.tokenizer import ChronicleQueryTokenizer


@parser_manager.register_supported_by_roota
class ChronicleQueryParser(PlatformQueryParser):
    mappings: ChronicleMappings = chronicle_query_mappings
    tokenizer: ChronicleQueryTokenizer = ChronicleQueryTokenizer()
    details: PlatformDetails = chronicle_query_details

    wrapped_with_comment_pattern = r"^\s*//.*(?:\n|$)"

    def parse(self, raw_query_container: RawQueryContainer) -> TokenizedQueryContainer:
        query_tokens = self.get_query_tokens(raw_query_container.query)
        field_tokens = self.get_field_tokens(query_tokens)
        source_mappings = self.get_source_mappings(field_tokens, {})
        meta_info = raw_query_container.meta_info
        meta_info.query_fields = field_tokens
        meta_info.source_mapping_ids = [source_mapping.source_id for source_mapping in source_mappings]
        return TokenizedQueryContainer(tokens=query_tokens, meta_info=meta_info)
