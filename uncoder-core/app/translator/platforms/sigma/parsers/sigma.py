"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2024 SOC Prime, Inc.

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


from typing import Union

from app.translator.core.exceptions.core import SigmaRuleValidationException
from app.translator.core.mixins.rule import YamlRuleMixin
from app.translator.core.models.field import FieldValue, Field
from app.translator.core.models.query_container import MetaInfoContainer, TokenizedQueryContainer, RawQueryContainer
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.parser import QueryParser
from app.translator.core.tokenizer import QueryTokenizer
from app.translator.platforms.sigma.const import SIGMA_RULE_DETAILS
from app.translator.platforms.sigma.mapping import SigmaMappings, sigma_mappings
from app.translator.platforms.sigma.tokenizer import SigmaConditionTokenizer, SigmaTokenizer


class SigmaParser(QueryParser, YamlRuleMixin):
    details: PlatformDetails = PlatformDetails(**SIGMA_RULE_DETAILS)
    condition_tokenizer = SigmaConditionTokenizer()
    tokenizer: SigmaTokenizer = SigmaTokenizer()
    mappings: SigmaMappings = sigma_mappings
    mandatory_fields = {"title", "description", "logsource", "detection"}

    wrapped_with_comment_pattern = r"^\s*#.*(?:\n|$)"

    @staticmethod
    def __parse_false_positives(false_positives: Union[str, list[str], None]) -> list:
        if isinstance(false_positives, str):
            return [i.strip() for i in false_positives.split(",")]
        return false_positives

    def _get_meta_info(
            self,
            rule: dict,
            source_mapping_ids: list[str],
            parsed_logsources: dict,
            fields_tokens: list[Field],
            sigma_fields_tokens: Union[list[Field], None] = None
    ) -> MetaInfoContainer:
        return MetaInfoContainer(
            title=rule.get("title"),
            id_=rule.get("id"),
            description=rule.get("description"),
            author=rule.get("author"),
            date=rule.get("date"),
            output_table_fields=sigma_fields_tokens,
            query_fields=fields_tokens,
            references=rule.get("references", []),
            license_=rule.get("license"),
            mitre_attack=self.parse_mitre_attack(rule.get("tags", [])),
            severity=rule.get("level"),
            status=rule.get("status"),
            tags=sorted(set(rule.get("tags", []))),
            false_positives=self.__parse_false_positives(rule.get("falsepositives")),
            source_mapping_ids=source_mapping_ids,
            parsed_logsources=parsed_logsources
        )

    def __validate_rule(self, rule: dict):
        if missing_fields := self.mandatory_fields.difference(set(rule.keys())):
            raise SigmaRuleValidationException(missing_fields=list(missing_fields))

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        return RawQueryContainer(query=text, language=language)

    def parse(self, raw_query_container: RawQueryContainer) -> TokenizedQueryContainer:
        sigma_rule = self.load_rule(text=raw_query_container.query)
        self.__validate_rule(rule=sigma_rule)
        log_sources = {
            key: [value]
            for key, value in (sigma_rule.get("logsource", {})).items()
            if key in ("product", "service", "category")
        }
        tokens = self.tokenizer.tokenize(detection=sigma_rule.get("detection"))
        field_tokens = [token.field for token in QueryTokenizer.filter_tokens(tokens, FieldValue)]
        field_names = [field.source_name for field in field_tokens]
        source_mappings = self.mappings.get_suitable_source_mappings(field_names=field_names, **log_sources)
        QueryTokenizer.set_field_tokens_generic_names_map(field_tokens, source_mappings, self.mappings.default_mapping)
        sigma_fields_tokens = None
        if sigma_fields := sigma_rule.get('fields'):
            sigma_fields_tokens = [Field(source_name=field) for field in sigma_fields]
            QueryTokenizer.set_field_tokens_generic_names_map(sigma_fields_tokens, source_mappings,
                                                              self.mappings.default_mapping)
        return TokenizedQueryContainer(
            tokens=tokens,
            meta_info=self._get_meta_info(
                rule=sigma_rule,
                source_mapping_ids=[source_mapping.source_id for source_mapping in source_mappings],
                sigma_fields_tokens=sigma_fields_tokens,
                parsed_logsources=log_sources,
                fields_tokens=field_tokens
            )
        )
