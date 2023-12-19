"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2023 SOC Prime, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------
"""


import re
from typing import List, Union

from app.translator.core.tokenizer import QueryTokenizer
from app.translator.platforms.sigma.const import SIGMA_RULE_DETAILS
from app.translator.platforms.sigma.mapping import SigmaMappings, sigma_mappings
from app.translator.platforms.sigma.tokenizer import SigmaTokenizer, SigmaConditionTokenizer
from app.translator.core.exceptions.core import SigmaRuleValidationException
from app.translator.core.mixins.rule import YamlRuleMixin
from app.translator.core.models.field import Field
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.parser_output import SiemContainer, MetaInfoContainer


class SigmaParser(YamlRuleMixin):
    details: PlatformDetails = PlatformDetails(**SIGMA_RULE_DETAILS)
    condition_tokenizer = SigmaConditionTokenizer()
    tokenizer: SigmaTokenizer = SigmaTokenizer()
    mappings: SigmaMappings = sigma_mappings
    mandatory_fields = {"title", "description", "logsource", "detection"}

    @staticmethod
    def __parse_false_positives(false_positives: Union[str, List[str], None]) -> list:
        if isinstance(false_positives, str):
            return [i.strip() for i in false_positives.split(',')]
        return false_positives

    def _get_meta_info(self, rule: dict, source_mapping_ids: List[str]) -> MetaInfoContainer:
        return MetaInfoContainer(
            title=rule.get("title"),
            id_=rule.get('id'),
            description=rule.get("description"),
            author=rule.get("author"),
            date=rule.get("date"),
            references=rule.get("references", []),
            license_=rule.get("license"),
            mitre_attack=self.parse_mitre_attack(rule.get("tags", [])),
            severity=rule.get("level"),
            status=rule.get("status"),
            tags=rule.get("tags"),
            false_positives=self.__parse_false_positives(rule.get("falsepositives")),
            source_mapping_ids=source_mapping_ids
        )

    def __validate_rule(self, rule: dict):
        if missing_fields := self.mandatory_fields.difference(set(rule.keys())):
            raise SigmaRuleValidationException(missing_fields=list(missing_fields))

    def parse(self, text: str) -> SiemContainer:
        sigma_rule = self.load_rule(text=text)
        self.__validate_rule(rule=sigma_rule)
        log_sources = {
            key: [value]
            for key, value in (sigma_rule.get("logsource", {})).items()
            if key in ("product", "service", "category")
        }
        tokens = self.tokenizer.tokenize(detection=sigma_rule.get("detection"))
        field_tokens = QueryTokenizer.filter_tokens(tokens, Field)
        field_names = [field.source_name for field in field_tokens]
        suitable_source_mappings = self.mappings.get_suitable_source_mappings(field_names=field_names, **log_sources)
        QueryTokenizer.set_field_generic_names_map(field_tokens, suitable_source_mappings, self.mappings)
        return SiemContainer(
            query=tokens,
            meta_info=self._get_meta_info(
                rule=sigma_rule,
                source_mapping_ids=[source_mapping.source_id for source_mapping in suitable_source_mappings]
            ),
        )
