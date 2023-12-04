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

from app.converter.core.exceptions.core import UnsupportedRootAParser, RootARuleValidationException
from app.converter.core.mixins.rule import YamlRuleMixin
from app.converter.core.models.parser_output import SiemContainer, MetaInfoContainer
from app.converter.core.parser import Parser
from app.converter.managers import parser_manager


class RootAParser(YamlRuleMixin):
    parsers = parser_manager
    mandatory_fields = {"name", "details", "author", "severity", "mitre-attack", "detection", "references", "license"}

    @staticmethod
    def __update_meta_info(meta_info: MetaInfoContainer, rule: dict) -> MetaInfoContainer:
        mitre_attack = rule.get("mitre-attack") or []
        mitre_attack = [i.strip("") for i in mitre_attack.split(",")] if isinstance(mitre_attack, str) else mitre_attack
        meta_info.title = rule.get("name")
        meta_info.description = rule.get("details")
        meta_info.id = rule.get("uuid", meta_info.id)
        meta_info.references = rule.get("references")
        meta_info.license = rule.get("license", meta_info.license)
        meta_info.tags = rule.get("tags", meta_info.tags)
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

    def __validate_rule(self, rule: dict):
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
