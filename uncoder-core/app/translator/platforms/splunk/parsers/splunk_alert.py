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

from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer, RawQueryContainer
from app.translator.managers import parser_manager
from app.translator.platforms.splunk.const import splunk_alert_details
from app.translator.platforms.splunk.mapping import SplunkMappings, splunk_alert_mappings
from app.translator.platforms.splunk.parsers.splunk import SplunkQueryParser


@parser_manager.register
class SplunkAlertParser(SplunkQueryParser):
    details: PlatformDetails = splunk_alert_details
    mappings: SplunkMappings = splunk_alert_mappings

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        severity = ""
        raw_mitre_attack: list[str] = []
        if severity_match := re.search(r"alert\.severity\s*=\s*(\d+)", text):
            severity = severity_match.group(1)
        if mitre_attack_match := re.search(r'"mitre_attack":\s*\[(.*?)\]', text):
            raw_mitre_attack = [attack.strip().strip('"') for attack in mitre_attack_match.group(1).split(",")]
        query = re.search(r"search\s*=\s*(?P<query>.+)", text).group("query")
        description = re.search(r"description\s*=\s*(?P<description>.+)", text).group("description")
        return RawQueryContainer(
            query=query,
            language=language,
            meta_info=MetaInfoContainer(description=description, severity=severity, raw_mitre_attack=raw_mitre_attack),
        )
