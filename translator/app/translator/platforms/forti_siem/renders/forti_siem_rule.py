import re
from typing import Optional, Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.custom_types.meta_info import SeverityType
from app.translator.core.custom_types.tokens import OperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.exceptions.render import UnsupportedRenderMethod
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.field import FieldValue
from app.translator.core.models.functions.base import ParsedFunctions
from app.translator.core.models.identifier import Identifier
from app.translator.core.models.parser_output import MetaInfoContainer
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseQueryFieldValue, BaseQueryRender
from app.translator.core.str_value_manager import StrValue
from app.translator.platforms.forti_siem.const import (
    FORTI_SIEM_RULE,
    SOURCES_EVENT_TYPES_CONTAINERS_MAP,
    forti_siem_rule_details,
)
from app.translator.platforms.forti_siem.mapping import FortiSiemMappings, forti_siem_mappings
from app.translator.platforms.forti_siem.str_value_manager import forti_siem_str_value_manager
from app.translator.tools.utils import concatenate_str

_EVENT_TYPE_FIELD = "eventType"

_SEVERITIES_MAP = {
    SeverityType.informational: "1",
    SeverityType.low: "3",
    SeverityType.medium: "5",
    SeverityType.high: "7",
    SeverityType.critical: "9",
}


class FortiSiemFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = forti_siem_rule_details
    str_value_manager = forti_siem_str_value_manager

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"

        if isinstance(value, StrValue):
            if value.has_spec_symbols:
                return self.regex_modifier(field, value)

            value = forti_siem_str_value_manager.from_container_to_str(value)
        return f'{field}="{value}"'

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        return f'{field}!="{value}"'

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.contains_modifier(field=field, value=v) for v in value])})"

        if isinstance(value, StrValue):
            value = forti_siem_str_value_manager.from_container_to_str(value, value_type=ValueType.regex_value)

        return f'{field} REGEXP "{value}"'

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.endswith_modifier(field=field, value=v) for v in value])})"

        if isinstance(value, StrValue):
            value = forti_siem_str_value_manager.from_container_to_str(value, value_type=ValueType.regex_value)

        return f'{field} REGEXP "{value}$"'

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.startswith_modifier(field=field, value=v) for v in value])})"

        if isinstance(value, StrValue):
            value = forti_siem_str_value_manager.from_container_to_str(value, value_type=ValueType.regex_value)

        return f'{field} REGEXP "^{value}"'

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.regex_modifier(field=field, value=v) for v in value])})"

        if isinstance(value, StrValue):
            value = forti_siem_str_value_manager.from_container_to_str(value, value_type=ValueType.regex_value)

        return f'{field} REGEXP "{value}"'

    def less_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method="<")

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method="<=")

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=">")

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method=">=")

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method="Keywords")


class FortiSiemRuleRender(BaseQueryRender):
    details: PlatformDetails = forti_siem_rule_details
    mappings: FortiSiemMappings = forti_siem_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    group_token = "(%s)"
    query_pattern = "{prefix} {query}"

    field_value_map = FortiSiemFieldValue(or_token=or_token)

    def generate(self, query: list, meta_info: MetaInfoContainer, functions: ParsedFunctions) -> str:
        queries_map = {}
        source_mappings = self._get_source_mappings(meta_info.source_mapping_ids)

        for source_mapping in source_mappings:
            is_event_type_set = False
            field_values = [token for token in query if isinstance(token, FieldValue)]
            mapped_fields_set = set()
            for field_value in field_values:
                mapped_fields = self.map_field(field_value.field, source_mapping)
                mapped_fields_set = mapped_fields_set.union(set(mapped_fields))
                if _EVENT_TYPE_FIELD in mapped_fields:
                    is_event_type_set = True
                    self.__update_event_type_values(field_value, source_mapping.source_id)

            result = self.generate_query(query=query, source_mapping=source_mapping)
            prefix = "" if is_event_type_set else self.generate_prefix(source_mapping.log_source_signature)
            finalized_query = self.finalize_query(
                prefix=prefix,
                query=result,
                functions=self.generate_functions(functions.functions, source_mapping),
                not_supported_functions=functions.not_supported,
                meta_info=meta_info,
                source_mapping=source_mapping,
                fields=mapped_fields_set,
            )
            queries_map[source_mapping.source_id] = finalized_query

        return self.finalize(queries_map)

    @staticmethod
    def __update_event_type_values(field_value: FieldValue, source_id: str) -> None:
        new_values = []
        for value in field_value.values:
            if not str(value).isdigit():
                new_values.append(value)

            elif not (source_event_types_container := SOURCES_EVENT_TYPES_CONTAINERS_MAP.get(source_id, {})):
                new_values.append(f"Win-.*-{value}[^\d]*")
                field_value.operator = Identifier(token_type=OperatorType.REGEX)

            elif event_types := source_event_types_container.event_types_map.get(value, []):
                new_values.extend(event_types)

            else:
                new_values.append(f"{source_event_types_container.default_pattern}{value}-.*")
                field_value.operator = Identifier(token_type=OperatorType.REGEX)

        field_value.values = new_values

    def finalize_query(
        self,
        prefix: str,
        query: str,
        functions: str,  # noqa: ARG002
        meta_info: Optional[MetaInfoContainer] = None,
        source_mapping: Optional[SourceMapping] = None,  # noqa: ARG002
        not_supported_functions: Optional[list] = None,
        fields: Optional[set[str]] = None,
        *args,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ) -> str:
        query = self.query_pattern.format(prefix=prefix, query=query).strip()
        rule = FORTI_SIEM_RULE.replace("<header_placeholder>", self.generate_rule_header(meta_info))
        rule = rule.replace("<name_placeholder>", self.generate_rule_name(meta_info.title))
        title = self.generate_title(meta_info.title)
        rule = rule.replace("<title_placeholder>", title)
        rule = rule.replace("<description_placeholder>", meta_info.description.replace("\n", " "))
        rule = rule.replace("<incident_def_placeholder>", self.generate_event_type(meta_info.title, meta_info.severity))
        args_list = self.get_args_list(fields.copy())
        rule = rule.replace("<args_list_placeholder>", self.get_args_str(args_list))
        rule = rule.replace("<query_placeholder>", query)
        rule = rule.replace("<group_by_attr_placeholder>", ", ".join(args_list))
        rule = rule.replace("<attr_list_placeholder>", self.get_attr_str(fields.copy()))

        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return rule + rendered_not_supported
        return rule

    @staticmethod
    def get_attr_str(fields: set[str]) -> str:
        fields.discard("hostName")
        fields.discard("eventType")
        fields.discard("phRecvTime")
        fields = sorted(fields)

        if len(fields) == 0:
            return "phRecvTime, rawEventMsg"

        return ", ".join(["phRecvTime", *fields, "rawEventMsg"])

    @staticmethod
    def get_args_str(fields: list[str]) -> str:
        return ", ".join(f"{f} = Filter.{f}" for f in fields)

    @staticmethod
    def get_args_list(fields: set[str]) -> list[str]:
        fields.discard("eventType")
        fields.add("hostName")
        return sorted(fields)

    @staticmethod
    def generate_event_type(title: str, severity: str) -> str:
        title = title.replace(" ", "_")
        return concatenate_str(f'eventType="PH_RULE_{title}"', f'severity="{_SEVERITIES_MAP[severity]}"')

    @staticmethod
    def generate_title(title: str) -> str:
        return re.sub(r"\s*[^a-zA-Z0-9 _-]+\s*", " ", title)

    @staticmethod
    def generate_rule_name(title: str) -> str:
        # rule name allows only a-zA-Z0-9 \/:.$-
        rule_name = re.sub(r'\s*[^a-zA-Z0-9 /:.$_\'"-]+\s*', " ", title)
        rule_name = re.sub("_", "-", rule_name)
        return re.sub(r'[\'"()+,]*', "", rule_name)

    @staticmethod
    def get_mitre_info(mitre_attack: dict) -> tuple[str, str]:
        tactics = set()
        techniques = set()
        for tactic in mitre_attack.get("tactics", []):
            if tactic_name := tactic.get("tactic"):
                tactics.add(tactic_name)

        for tech in mitre_attack.get("techniques", []):
            techniques.add(tech["technique_id"])
            tactics = tactics.union(set(tech.get("tactic", [])))

        return ", ".join(sorted(tactics)), ", ".join(sorted(techniques))

    def generate_rule_header(self, meta_info: MetaInfoContainer) -> str:
        header = 'group="PH_SYS_RULE_THREAT_HUNTING"'
        header = concatenate_str(header, f'id="{meta_info.id}"')
        tactics_str, techniques_str = self.get_mitre_info(meta_info.mitre_attack)
        if tactics_str:
            header = concatenate_str(header, f'subFunction="{tactics_str}"')

        if techniques_str:
            header = concatenate_str(header, f'technique="{techniques_str}"')

        return concatenate_str(header, 'phIncidentCategory="Server" function="Security"')

    def wrap_with_comment(self, value: str) -> str:
        return f"<!-- {value} -->"
