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

from typing import ClassVar

from app.translator.core.exceptions.core import RootARuleValidationException, UnsupportedRootAParser
from app.translator.core.mixins.rule import YamlRuleMixin
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer, RawQueryContainer, TokenizedQueryContainer
from app.translator.core.parser import PlatformQueryParser, QueryParser
from app.translator.managers import parser_manager
from app.translator.platforms.roota.const import ROOTA_RULE_DETAILS


@parser_manager.register_parser
class RootAParser(QueryParser, YamlRuleMixin):
    parser_manager = parser_manager
    details: PlatformDetails = PlatformDetails(**ROOTA_RULE_DETAILS)
    mandatory_fields: ClassVar[set[str]] = {
        "name",
        "details",
        "author",
        "severity",
        "mitre-attack",
        "detection",
        "references",
        "license",
    }

    def __parse_meta_info(self, rule: dict) -> MetaInfoContainer:
        mitre_attack = rule.get("mitre-attack") or []
        mitre_tags = [i.strip("") for i in mitre_attack.split(",")] if isinstance(mitre_attack, str) else mitre_attack
        mitre_attack = self.parse_mitre_attack(mitre_tags)
        rule_tags = rule.get("tags", [])
        if isinstance(rule_tags, str):
            rule_tags = [i.strip() for i in rule_tags.split(",")]
        rule_tags += mitre_tags

        return MetaInfoContainer(
            id_=rule.get("uuid"),
            title=rule.get("name"),
            description=rule.get("details"),
            author=rule.get("author"),
            date=rule.get("date"),
            license_=rule.get("license"),
            severity=rule.get("severity"),
            references=rule.get("references"),
            mitre_attack=mitre_attack,
            tags=rule_tags,
        )

    def __get_parser_class(self, parser: str) -> PlatformQueryParser:
        parser_class = self.parser_manager.get_roota_parser(parser)
        if parser_class:
            return parser_class
        raise UnsupportedRootAParser(parser=parser)

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        rule = self.load_rule(text=text)
        if missing_fields := self.mandatory_fields.difference(set(rule.keys())):
            raise RootARuleValidationException(missing_fields=list(missing_fields))

        detection = rule.get("detection", {})
        query = detection.get("body")
        language = detection.get("language")
        if not (query or language):
            raise RootARuleValidationException(missing_fields=["detection"])

        return RawQueryContainer(query=query, language=language, meta_info=self.__parse_meta_info(rule))

    def parse(self, raw_query_container: RawQueryContainer) -> TokenizedQueryContainer:
        parser = self.__get_parser_class(raw_query_container.language)
        return parser.parse(raw_query_container)
