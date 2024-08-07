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
from app.translator.platforms.logscale.const import logscale_alert_details
from app.translator.platforms.logscale.mapping import LogScaleMappings, logscale_alert_mappings
from app.translator.platforms.logscale.parsers.logscale import LogScaleQueryParser
from app.translator.tools.utils import parse_rule_description_str


@parser_manager.register
class LogScaleAlertParser(LogScaleQueryParser, JsonRuleMixin):
    details: PlatformDetails = logscale_alert_details
    mappings: LogScaleMappings = logscale_alert_mappings

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        rule = self.load_rule(text=text)
        parsed_description = parse_rule_description_str(rule["description"])
        return RawQueryContainer(
            query=rule["query"]["queryString"],
            language=language,
            meta_info=MetaInfoContainer(
                id_=parsed_description.get("rule_id"),
                author=parsed_description.get("author"),
                references=parsed_description.get("references"),
                title=rule.get("name"),
                description=parsed_description.get("description") or rule.get("description"),
            ),
        )
