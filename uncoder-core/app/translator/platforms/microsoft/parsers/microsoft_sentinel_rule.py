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
        return RawQueryContainer(
            query=rule["query"],
            language=language,
            meta_info=MetaInfoContainer(
                title=rule.get("displayName"),
                description=rule.get("description"),
                timeframe=self.__parse_timeframe(rule.get("queryFrequency", "")),
            ),
        )
