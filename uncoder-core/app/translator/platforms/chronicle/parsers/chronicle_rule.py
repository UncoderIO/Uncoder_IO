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

from app.translator.core.exceptions.parser import TokenizerGeneralException
from app.translator.core.mitre import MitreConfig, MitreInfoContainer
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer, RawQueryContainer
from app.translator.managers import parser_manager
from app.translator.platforms.chronicle.const import chronicle_rule_details
from app.translator.platforms.chronicle.mapping import ChronicleMappings, chronicle_rule_mappings
from app.translator.platforms.chronicle.parsers.chronicle import ChronicleQueryParser
from app.translator.platforms.chronicle.tokenizer import ChronicleRuleTokenizer


@parser_manager.register
class ChronicleRuleParser(ChronicleQueryParser):
    details: PlatformDetails = chronicle_rule_details
    rule_name_pattern = r"rule\s+(?P<rule_name>[a-zA-Z0-9_]+)\s+{"
    meta_info_pattern = r"meta:\n(?P<meta_info>[a-zA-Z0-9_\\\.*,>–<—~#$’`:;%+^\|?!@\s\"/=\-&'\(\)\[\]]+)\n\s+events:"  # noqa: RUF001
    rule_pattern = r"events:\n\s*(?P<query>[a-zA-Z\w0-9_%{}\|\.,!#^><:~\s\"\/=+?\-–&;$()`\*@\[\]'\\]+)\n\s+condition:"  # noqa: RUF001
    event_name_pattern = r"condition:\n\s*(?P<event_name>\$[a-zA-Z_0-9]+)\n"
    mappings: ChronicleMappings = chronicle_rule_mappings
    tokenizer = ChronicleRuleTokenizer()
    mitre_config: MitreConfig = MitreConfig()

    def __parse_rule(self, rule: str) -> tuple[str, str, str]:
        if (rule_name_search := re.search(self.rule_name_pattern, rule)) is None:
            raise TokenizerGeneralException(error="Rule name couldn't be found in rule.")
        rule_name = rule_name_search.group("rule_name")

        if (meta_info_search := re.search(self.meta_info_pattern, rule)) is None:
            raise TokenizerGeneralException(error="Rule meta info couldn't be found in rule.")
        meta_info = meta_info_search.group("meta_info")

        if (query_search := re.search(self.rule_pattern, rule)) is None:
            raise TokenizerGeneralException(error="Query couldn't be found in rule.")
        query = query_search.group("query")

        if (event_name_search := re.search(self.event_name_pattern, rule)) is None:
            raise TokenizerGeneralException(error="Event name couldn't be found in rule.")
        event_name = event_name_search.group("event_name")

        query = query.replace(f"{event_name}.", "")
        return query.strip(" ").strip("\n"), rule_name, meta_info

    @staticmethod
    def __prepare_title(name: str) -> str:
        return " ".join(name.split("_")).title()

    @staticmethod
    def __parse_meta_info(meta_info_str: str) -> dict:
        parsed_meta_info = {}

        for info in meta_info_str.strip(" ").strip("\n").split("\n"):
            key, value = info.split(" = ")
            key = key.strip(" ")
            if key in ("description", "license", "version", "sigma_id", "status", "severity", "created"):
                parsed_meta_info[key] = value.strip(" ").strip('"')
            elif key == "reference":
                parsed_meta_info[key] = [value.strip(" ").strip('"')]
            elif key in ("tags", "author"):
                parsed_meta_info[key] = [i.strip(" ").strip('"') for i in value.split(",")]

        return parsed_meta_info

    def parse_mitre_attack_from_tags(self, tags: list) -> MitreInfoContainer:
        parsed_techniques = []
        parsed_tactics = []
        for tag in set(tags):
            tag = tag.lower()
            if tag.startswith("attack."):
                tag = tag[7::]
            if tag[-1].isdigit():
                parsed_techniques.append(tag)
            else:
                parsed_tactics.append(tag)
        return self.mitre_config.get_mitre_info(tactics=parsed_tactics, techniques=parsed_techniques)

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        query, rule_name, meta_info_str = self.__parse_rule(text)
        parsed_meta_info = self.__parse_meta_info(meta_info_str)

        return RawQueryContainer(
            query=query,
            language=language,
            meta_info=MetaInfoContainer(
                id_=parsed_meta_info.get("sigma_id"),
                title=self.__prepare_title(rule_name),
                description=parsed_meta_info.get("description"),
                author=parsed_meta_info.get("author"),
                date=parsed_meta_info.get("created"),
                license_=parsed_meta_info.get("license"),
                severity=parsed_meta_info.get("severity"),
                references=parsed_meta_info.get("reference"),
                tags=parsed_meta_info.get("tags"),
                status=parsed_meta_info.get("status"),
                mitre_attack=self.parse_mitre_attack_from_tags(parsed_meta_info.get("tags") or []),
            ),
        )
