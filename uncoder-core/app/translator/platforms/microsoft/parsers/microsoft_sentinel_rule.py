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

from contextlib import suppress
from datetime import timedelta
from typing import Optional

import isodate
from isodate.isoerror import ISO8601Error

from app.translator.core.mixins.rule import JsonRuleMixin
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer, RawQueryContainer
from app.translator.managers import parser_manager
from app.translator.platforms.microsoft.const import microsoft_sentinel_rule_details
from app.translator.platforms.microsoft.mapping import MicrosoftSentinelMappings, microsoft_sentinel_rule_mappings
from app.translator.platforms.microsoft.parsers.microsoft_sentinel import MicrosoftSentinelQueryParser
from app.translator.tools.utils import parse_rule_description_str


@parser_manager.register
class MicrosoftSentinelRuleParser(MicrosoftSentinelQueryParser, JsonRuleMixin):
    details: PlatformDetails = microsoft_sentinel_rule_details
    mappings: MicrosoftSentinelMappings = microsoft_sentinel_rule_mappings

    @staticmethod
    def __parse_timeframe(raw_timeframe: Optional[str]) -> Optional[timedelta]:
        with suppress(ISO8601Error):
            return isodate.parse_duration(raw_timeframe)

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        rule = self.load_rule(text=text)
        mitre_attack = {
            "tactics": [self.mitre_config.get_tactic(tactic.lower()) for tactic in rule.get("tactics", [])],
            "techniques": [self.mitre_config.get_technique(tactic.lower()) for tactic in rule.get("techniques", [])],
        }
        parsed_description = parse_rule_description_str(rule.get("description", ""))

        return RawQueryContainer(
            query=rule["query"],
            language=language,
            meta_info=MetaInfoContainer(
                title=rule.get("displayName"),
                description=parsed_description.get("description") or rule.get("description"),
                timeframe=self.__parse_timeframe(rule.get("queryFrequency", "")),
                severity=rule.get("severity", "medium"),
                mitre_attack=mitre_attack if mitre_attack["tactics"] or mitre_attack["techniques"] else None,
                author=parsed_description.get("author") or rule.get("author", ""),
                license_=parsed_description.get("license"),
            ),
        )
