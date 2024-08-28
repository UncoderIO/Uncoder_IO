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
from datetime import datetime

from app.translator.core.mixins.rule import JsonRuleMixin, TOMLRuleMixin
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer, RawMetaInfoContainer, RawQueryContainer
from app.translator.managers import parser_manager
from app.translator.platforms.elasticsearch.const import elasticsearch_rule_details, elasticsearch_rule_toml_details
from app.translator.platforms.elasticsearch.parsers.elasticsearch import ElasticSearchQueryParser
from app.translator.tools.utils import parse_rule_description_str


@parser_manager.register
class ElasticSearchRuleParser(ElasticSearchQueryParser, JsonRuleMixin):
    details: PlatformDetails = elasticsearch_rule_details

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        rule = self.load_rule(text=text)
        parsed_description = parse_rule_description_str(rule.get("description", ""))

        mitre_attack = self.mitre_config.get_mitre_info(
            tactics=[threat_data["tactic"]["name"].replace(" ", "_").lower() for threat_data in rule.get("threat", [])],
            techniques=[threat_data["technique"][0]["id"].lower() for threat_data in rule.get("threat", [])],
        )

        return RawQueryContainer(
            query=rule["query"],
            language=language,
            meta_info=MetaInfoContainer(
                id_=rule.get("rule_id"),
                title=rule.get("name"),
                description=parsed_description.get("description") or rule.get("description"),
                references=rule.get("references", []),
                author=parsed_description.get("author") or rule.get("author"),
                severity=rule.get("severity"),
                license_=parsed_description.get("license"),
                tags=rule.get("tags"),
                mitre_attack=mitre_attack,
            ),
        )


@parser_manager.register
class ElasticSearchRuleTOMLParser(ElasticSearchQueryParser, TOMLRuleMixin):
    details: PlatformDetails = elasticsearch_rule_toml_details

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        raw_rule = self.load_rule(text=text)
        rule = raw_rule.get("rule")
        metadata = raw_rule.get("metadata")
        techniques = []
        for threat_data in rule.get("threat", []):
            if len(threat_data.get("technique", [])) > 0:
                techniques.append(threat_data["technique"][0]["id"].lower())
        mitre_attack = self.mitre_config.get_mitre_info(
            tactics=[threat_data["tactic"]["name"].replace(" ", "_").lower() for threat_data in rule.get("threat", [])],
            techniques=techniques,
        )
        date = None
        if metadata.get("creation_date"):
            date = datetime.strptime(metadata.get("creation_date"), "%Y/%m/%d").strftime("%Y-%m-%d")
        return RawQueryContainer(
            query=rule["query"],
            language=language,
            meta_info=MetaInfoContainer(
                id_=rule.get("rule_id"),
                title=rule.get("name"),
                description=rule.get("description"),
                author=rule.get("author"),
                date=date,
                license_=rule.get("license"),
                severity=rule.get("severity"),
                references=rule.get("references"),
                tags=rule.get("tags"),
                mitre_attack=mitre_attack,
                index=rule.get("index"),
                language=rule.get("language"),
                risk_score=rule.get("risk_score"),
                type_=rule.get("type"),
                raw_metainfo_container=RawMetaInfoContainer(from_=rule.get("from"), interval=rule.get("interval")),
            ),
        )
