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

import re

from app.translator.core.custom_types.meta_info import SeverityType
from app.translator.core.mitre import MitreConfig
from app.translator.core.mixins.rule import YamlRuleMixin
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer, MitreInfoContainer, RawQueryContainer
from app.translator.managers import parser_manager
from app.translator.platforms.splunk.const import splunk_alert_details, splunk_alert_yml_details
from app.translator.platforms.splunk.mapping import SplunkMappings, splunk_alert_mappings
from app.translator.platforms.splunk.parsers.splunk import SplunkQueryParser


@parser_manager.register
class SplunkAlertParser(SplunkQueryParser):
    details: PlatformDetails = splunk_alert_details
    mappings: SplunkMappings = splunk_alert_mappings
    mitre_config: MitreConfig = MitreConfig()

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        rule_id: str = ""
        rule_name: str = ""
        severity: str = ""
        mitre_attack_container: MitreInfoContainer = None
        if severity_match := re.search(r"alert\.severity\s*=\s*(\d+)", text):
            level_map = {
                "1": SeverityType.low,
                "2": SeverityType.medium,
                "3": SeverityType.high,
                "4": SeverityType.critical,
            }
            severity = level_map.get(str(severity_match.group(1)), "low")

        if mitre_attack_match := re.search(r"'mitre_attack':\s*\[(.*?)\]", text):
            raw_mitre_attack = [attack.strip().strip("'") for attack in mitre_attack_match.group(1).split(",")]
            mitre_attack_container = self.mitre_config.get_mitre_info(
                tactics=[i.lower() for i in raw_mitre_attack if not i[-1].isdigit()],
                techniques=[i.lower() for i in raw_mitre_attack if i[-1].isdigit()],
            )

        if rule_id_match := re.search(r"Rule ID:\s*([\w-]+)", text):
            rule_id = rule_id_match.group(1)
        if rule_name_match := re.search(r"action\.notable\.param\.rule_title\s*=\s*(.*)", text):
            rule_name = rule_name_match.group(1)

        query = re.search(r"search\s*=\s*(?P<query>.+)", text).group("query")
        description = re.search(r"description\s*=\s*(?P<description>.+)", text).group("description")
        return RawQueryContainer(
            query=query,
            language=language,
            meta_info=MetaInfoContainer(
                id_=rule_id,
                title=rule_name,
                description=description,
                severity=severity,
                mitre_attack=mitre_attack_container,
            ),
        )


@parser_manager.register
class SplunkAlertYMLParser(SplunkQueryParser, YamlRuleMixin):
    details: PlatformDetails = splunk_alert_yml_details
    mappings: SplunkMappings = splunk_alert_mappings
    mitre_config: MitreConfig = MitreConfig()

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        rule = self.load_rule(text)
        mitre_attack_container = self.mitre_config.get_mitre_info(
            techniques=rule.get("tags", {}).get("mitre_attack_id", [])
        )
        description = rule.get("description", "")
        if rule.get("how_to_implement", ""):
            description = f'{description} {rule.get("how_to_implement", "")}'
        tags = rule.get("tags", {}).get("analytic_story", [])
        if rule.get("type"):
            tags.append(rule.get("type"))
        false_positives = None
        if rule.get("known_false_positives"):
            false_positives = (
                rule["known_false_positives"]
                if isinstance(rule["known_false_positives"], list)
                else [rule["known_false_positives"]]
            )
        return RawQueryContainer(
            query=rule.get("search"),
            language=language,
            meta_info=MetaInfoContainer(
                id_=rule.get("id"),
                title=rule.get("name"),
                date=rule.get("date"),
                author=rule.get("author").split(", "),
                status=rule.get("status"),
                description=description,
                false_positives=false_positives,
                references=rule.get("references"),
                mitre_attack=mitre_attack_container,
                tags=tags,
            ),
        )
