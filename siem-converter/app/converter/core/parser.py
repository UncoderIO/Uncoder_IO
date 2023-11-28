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

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from app.converter.core.mapping import BasePlatformMappings, SourceMapping
from app.converter.core.models.field import Field
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.models.parser_output import SiemContainer, MetaInfoContainer
from app.converter.core.tokenizer import QueryTokenizer, TOKEN_TYPE


class Parser(ABC):
    mappings: BasePlatformMappings = None
    tokenizer: QueryTokenizer = None
    details: PlatformDetails = None

    @abstractmethod
    def _get_meta_info(self, *args, **kwargs) -> MetaInfoContainer:
        raise NotImplementedError("Abstract method")

    @abstractmethod
    def parse(self, text: str) -> SiemContainer:
        raise NotImplementedError("Abstract method")

    def get_tokens_and_source_mappings(self,
                                       query: str,
                                       log_sources: Dict[str, List[str]]
                                       ) -> Tuple[List[TOKEN_TYPE], List[SourceMapping]]:
        tokens = self.tokenizer.tokenize(query=query)
        field_tokens = self.tokenizer.filter_tokens(tokens, Field)
        field_names = [field.source_name for field in field_tokens]
        suitable_source_mappings = self.mappings.get_suitable_source_mappings(field_names=field_names, **log_sources)
        self.tokenizer.set_field_generic_names_map(field_tokens, suitable_source_mappings, self.mappings)

        return tokens, suitable_source_mappings
