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

from app.converter.backends.logscale.const import logscale_alert_details
from app.converter.backends.logscale.parsers.logscale import LogScaleParser
from app.converter.core.mixins.rule import JsonRuleMixin
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.operator_types.output import SiemContainer, MetaInfoContainer


class LogScaleAlertParser(LogScaleParser, JsonRuleMixin):
    details: PlatformDetails = logscale_alert_details

    def _parse_rule(self, text: str):
        rule = self.load_rule(text=text)
        query = rule['query']['queryString']
        description = rule['description']
        name = rule['name']
        return {
            'query': query,
            'name': name,
            'description': description
        }

    @staticmethod
    def _get_meta_info(source_mapping_ids: List[str], meta_info: dict) -> MetaInfoContainer:
        return MetaInfoContainer(
            title=meta_info['name'],
            description=meta_info['description'],
            source_mapping_ids=source_mapping_ids
        )

    def parse(self, text: str) -> SiemContainer:
        parsed_rule = self._parse_rule(text)
        query, functions = self._parse_query(query=parsed_rule.pop("query"))
        tokens, source_mappings = self.get_tokens_and_source_mappings(text, {})
        return SiemContainer(
            query=tokens,
            meta_info=self._get_meta_info(
                meta_info=parsed_rule,
                source_mapping_ids=[source_mapping.source_id for source_mapping in source_mappings]
            ),
            functions=functions
        )
