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

from typing import List, Dict

from app.translator.platforms.elasticsearch.const import elasticsearch_rule_details
from app.translator.platforms.elasticsearch.parsers.elasticsearch import ElasticSearchParser
from app.translator.core.mixins.rule import JsonRuleMixin
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.parser_output import SiemContainer, MetaInfoContainer


class ElasticSearchRuleParser(ElasticSearchParser, JsonRuleMixin):
    details: PlatformDetails = elasticsearch_rule_details

    def _parse_rule(self, text: str) -> Dict:
        rule = self.load_rule(text=text)
        query = rule['query']
        description = rule['description']
        name = rule['name']
        return {
            'query': query,
            'title': name,
            'description': description
        }

    @staticmethod
    def _get_meta_info(source_mapping_ids: List[str], meta_info: dict) -> MetaInfoContainer:
        return MetaInfoContainer(
            title=meta_info['title'],
            description=meta_info['description'],
            source_mapping_ids=source_mapping_ids
        )

    def parse(self, text: str) -> SiemContainer:
        rule, log_sources = self._parse_rule(text)
        tokens, source_mappings = self.get_tokens_and_source_mappings(rule.get("query"), log_sources)
        return SiemContainer(
            query=tokens,
            meta_info=self._get_meta_info(
                source_mapping_ids=[source_mapping.source_id for source_mapping in source_mappings],
                meta_info=rule
            ),
        )
