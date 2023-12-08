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

import re
from typing import List, Dict

from app.translator.platforms.chronicle.const import chronicle_rule_details
from app.translator.platforms.chronicle.mapping import ChronicleMappings, chronicle_mappings
from app.translator.platforms.chronicle.tokenizer import ChronicleRuleTokenizer
from app.translator.core.exceptions.parser import TokenizerGeneralException
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.parser import Parser
from app.translator.core.models.parser_output import SiemContainer, MetaInfoContainer


class ChronicleRuleParser(Parser):
    details: PlatformDetails = chronicle_rule_details
    rule_name_pattern = "rule\s(?P<rule_name>[a-z0-9_]+)\s{"
    meta_info_pattern = "meta:\n(?P<meta_info>[a-zA-Z0-9_\\\.*,>–<—~#$’`:;%+^\|?!@\s\"/=\-&'\(\)\[\]]+)\n\s+events:"
    rule_pattern = "events:\n\s*(?P<rule>[a-zA-Z\w0-9_%{}\|\.,!#^><:~\s\"\/=+?\-–&;$()`\*@\[\]'\\\]+)\n\s+condition:"
    event_name_pattern = "condition:\n\s*(?P<event_name>\$[a-zA-Z_0-9]+)\n"
    mappings: ChronicleMappings = chronicle_mappings
    tokenizer = ChronicleRuleTokenizer()

    def __parse_rule(self, rule) -> Dict:
        rule_name_search = re.search(self.rule_name_pattern, rule)
        if rule_name_search is None:
            raise TokenizerGeneralException(error=f"Field couldn't be found in rule.")
        rule_name = rule_name_search.group("rule_name")

        meta_info_search = re.search(self.meta_info_pattern, rule)
        if meta_info_search is None:
            raise TokenizerGeneralException(error=f"Rule meta info couldn't be found in rule.")
        meta_info = meta_info_search.group("meta_info")

        query_search = re.search(self.rule_pattern, rule)
        if query_search is None:
            raise TokenizerGeneralException(error=f"Query couldn't be found in rule.")
        query = query_search.group("rule")

        event_name_search = re.search(self.event_name_pattern, rule)
        if query_search is None:
            raise TokenizerGeneralException(error=f"Event name couldn't be found in rule.")
        event_name = event_name_search.group("event_name")

        query = query.replace(f"{event_name}.", "")
        return {"query": query.strip(" ").strip("\n"), "rule_name": rule_name, "meta_info": meta_info}

    @staticmethod
    def __prepare_title(name) -> str:
        return " ".join(name.split("_")).title()

    def _get_meta_info(self, rule_name: str, source_mapping_ids: List[str], meta_info: str) -> MetaInfoContainer:
        references = tags = []
        description = None
        for info in meta_info.strip(" ").strip("\n").split("\n"):
            key, value = info.split(" = ")
            key = key.strip(" ")
            if key == "reference":
                references = [value.strip(" ").strip('"')]
            elif key == "description":
                description = value.strip(" ")
            elif key == "tags":
                tags = [i.strip(" ").strip('"') for i in value.split(",")]

        return MetaInfoContainer(
            title=self.__prepare_title(rule_name),
            source_mapping_ids=source_mapping_ids,
            references=references,
            tags=tags,
            description=description
        )

    def parse(self, text: str) -> SiemContainer:
        parsed_rule = self.__parse_rule(text)
        tokens, source_mappings = self.get_tokens_and_source_mappings(parsed_rule.get("query"), {})
        return SiemContainer(
            query=tokens,
            meta_info=self._get_meta_info(
                rule_name=parsed_rule.get("rule_name"),
                meta_info=parsed_rule.get("meta_info"),
                source_mapping_ids=[source_mapping.source_id for source_mapping in source_mappings]
            ),
        )
