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

from app.translator.core.mixins.rule import JsonRuleMixin
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer, RawQueryContainer
from app.translator.managers import parser_manager
from app.translator.platforms.elasticsearch.const import elasticsearch_rule_details
from app.translator.platforms.elasticsearch.parsers.elasticsearch import ElasticSearchQueryParser


@parser_manager.register
class ElasticSearchRuleParser(ElasticSearchQueryParser, JsonRuleMixin):
    details: PlatformDetails = elasticsearch_rule_details

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        rule = self.load_rule(text=text)
        return RawQueryContainer(
            query=rule["query"],
            language=language,
            meta_info=MetaInfoContainer(
                id_=rule["rule_id"],
                title=rule["name"],
                description=rule["description"],
                references=rule.get("references", []),
                author=rule["author"],
                severity=rule["severity"],
                tags=rule["tags"],
            ),
        )
