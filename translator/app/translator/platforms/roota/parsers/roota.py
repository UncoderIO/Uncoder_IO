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

from typing import ClassVar

from app.translator.core.exceptions.core import RootARuleValidationException, UnsupportedRootAParser
from app.translator.core.mixins.rule import YamlRuleMixin
from app.translator.core.models.parser_output import MetaInfoContainer, SiemContainer
from app.translator.core.parser import Parser
from app.translator.managers import parser_manager


class RootAParser(YamlRuleMixin):
    parsers = parser_manager
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

    def __update_meta_info(self, meta_info: MetaInfoContainer, rule: dict) -> MetaInfoContainer:
        mitre_attack = rule.get("mitre-attack") or []
        mitre_tags = [i.strip("") for i in mitre_attack.split(",")] if isinstance(mitre_attack, str) else mitre_attack
        mitre_attack = self.parse_mitre_attack(mitre_tags)
        rule_tags = rule.get("tags", [])
        rule_tags += mitre_tags

        meta_info.title = rule.get("name")
        meta_info.description = rule.get("details")
        meta_info.id = rule.get("uuid", meta_info.id)
        meta_info.references = rule.get("references")
        meta_info.license = rule.get("license", meta_info.license)
        meta_info.tags = rule_tags or meta_info.tags
        meta_info.mitre_attack = mitre_attack
        meta_info.date = rule.get("date", meta_info.date)
        meta_info.author = rule.get("author", meta_info.author)
        meta_info.severity = rule.get("severity", meta_info.severity)
        return meta_info

    def _get_parser_class(self, parser: str) -> Parser:
        parser_class = self.parsers.get(parser)
        if parser_class:
            return parser_class
        raise UnsupportedRootAParser(parser=parser)

    def __validate_rule(self, rule: dict) -> None:
        if missing_fields := self.mandatory_fields.difference(set(rule.keys())):
            raise RootARuleValidationException(missing_fields=list(missing_fields))

    def parse(self, text: str) -> SiemContainer:
        roota_rule = self.load_rule(text=text)
        self.__validate_rule(rule=roota_rule)
        detection = roota_rule.get("detection", {}).get("body", "")
        parser = self._get_parser_class(roota_rule.get("detection", {}).get("language", ""))
        siem_container = parser.parse(text=detection)
        siem_container.meta_info = self.__update_meta_info(meta_info=siem_container.meta_info, rule=roota_rule)
        return siem_container
