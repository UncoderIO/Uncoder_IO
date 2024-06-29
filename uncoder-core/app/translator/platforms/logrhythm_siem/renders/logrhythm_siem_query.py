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
import json
from typing import Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.context_vars import return_only_first_query_ctx_var
from app.translator.core.custom_types.tokens import LogicalOperatorType
from app.translator.core.custom_types.values import ValueType
from app.translator.core.exceptions.core import StrictPlatformException
from app.translator.core.exceptions.render import BaseRenderException
from app.translator.core.mapping import LogSourceSignature, SourceMapping
from app.translator.core.models.field import FieldValue, Keyword
from app.translator.core.models.identifier import Identifier
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import TokenizedQueryContainer
from app.translator.core.render import BaseQueryFieldValue, PlatformQueryRender
from app.translator.managers import render_manager
# from app.translator.platforms.logrhythm_siem.const import UNMAPPED_FIELD_DEFAULT_NAME, logrhythm_siem_query_details
from app.translator.platforms.logrhythm_siem.const import UNMAPPED_FIELD_DEFAULT_NAME, logrhythm_siem_rule_details
from app.translator.platforms.logrhythm_siem.escape_manager import logrhythm_query_escape_manager
from app.translator.platforms.logrhythm_siem.mapping import LogRhythmSiemMappings, logrhythm_siem_mappings


class LogRhythmRegexRenderException(BaseRenderException):
    ...


class LogRhythmSiemFieldValue(BaseQueryFieldValue):
    # details: PlatformDetails = logrhythm_siem_query_details
    details: PlatformDetails = logrhythm_siem_rule_details
    escape_manager = logrhythm_query_escape_manager

    def __is_complex_regex(self, regex: str) -> bool:
        regex_items = ("[", "]", "(", ")", "{", "}", "+", "?", "^", "$", "\\d", "\\w", "\\s", "-")
        return any(v in regex for v in regex_items)

    def __is_contain_regex_items(self, value: str) -> bool:
        regex_items = ("[", "]", "(", ")", "{", "}", "*", "+", "?", "^", "$", "|", ".", "\\d", "\\w", "\\s", "\\", "-")
        return any(v in value for v in regex_items)

    def __regex_to_str_list(self, value: Union[int, str]) -> list[list[str]]:  # noqa: PLR0912
        value_groups = []

        stack = []  # [(element: str, escaped: bool)]

        for char in value:
            if char == "\\":
                if stack and stack[-1][0] == "\\" and stack[-1][1] is False:
                    stack.pop()
                    stack.append((char, True))
                else:
                    stack.append(("\\", False))
            elif char == "|":
                if stack and stack[-1][0] == "\\" and stack[-1][1] is False:
                    stack.pop()
                    stack.append((char, True))
                elif stack:
                    value_groups.append("".join(element[0] for element in stack))
                    stack = []
            else:
                stack.append((char, False))
        if stack:
            value_groups.append("".join(element[0] for element in stack if element[0] != "\\" or element[-1] is True))

        joined_components = []
        for value_group in value_groups:
            inner_joined_components = []
            not_joined_components = []
            for i in range(len(value_group)):
                if value_group[i] == "*" and i > 0 and value_group[i - 1] != "\\":
                    inner_joined_components.append("".join(not_joined_components))
                    not_joined_components = []
                else:
                    not_joined_components.append(value_group[i])
            if not_joined_components:
                inner_joined_components.append("".join(not_joined_components))
            joined_components.append(inner_joined_components)

        return joined_components

    def __unmapped_regex_field_to_contains_string(self, field: str, value: str) -> str:
        if self.__is_complex_regex(value):
            raise LogRhythmRegexRenderException
        values = self.__regex_to_str_list(value)
        return (
            "("
            + self.or_token.join(
                " AND ".join(f'{field} CONTAINS "{self.apply_value(value)}"' for value in value_list)
                for value_list in values
            )
            + ")"
        )

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if field == UNMAPPED_FIELD_DEFAULT_NAME:
            return self.contains_modifier(field, value)
        if isinstance(value, str):
            return f'{field} = "{self.apply_value(value)}"'
        if isinstance(value, list):
            prepared_values = ", ".join(f"{self.apply_value(v)}" for v in value)
            operator = "IN" if all(isinstance(v, str) for v in value) else "in"
            return f"{field} {operator} [{prepared_values}]"
        return f'{field} = "{self.apply_value(value)}"'

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        if field == UNMAPPED_FIELD_DEFAULT_NAME:
            return self.contains_modifier(field, value)
        if isinstance(value, int):
            return f"{field} < {value}"
        return f"{field} < '{self.apply_value(value)}'"

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        if field == UNMAPPED_FIELD_DEFAULT_NAME:
            return self.contains_modifier(field, value)
        if isinstance(value, int):
            return f"{field} <= {value}"
        return f"{field} <= {self.apply_value(value)}"

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        if field == UNMAPPED_FIELD_DEFAULT_NAME:
            return self.contains_modifier(field, value)
        if isinstance(value, int):
            return f"{field} > {value}"
        return f"{field} > {self.apply_value(value)}"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        if field == UNMAPPED_FIELD_DEFAULT_NAME:
            return self.contains_modifier(field, value)
        if isinstance(value, int):
            return f"{field} >= {value}"
        return f"{field} >= {self.apply_value(value)}"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if field == UNMAPPED_FIELD_DEFAULT_NAME:
            return self.contains_modifier(field, value)
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        if isinstance(value, int):
            return f"{field} != {value}"
        return f"{field} != {self.apply_value(value)}"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE):
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f'{field} CONTAINS "{self.apply_value(value)}"'

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        if isinstance(value, str) and field == UNMAPPED_FIELD_DEFAULT_NAME:
            return self.contains_modifier(field, value)
        applied_value = self.apply_value(value, value_type=ValueType.regex_value)
        return f'{field} matches ".*{applied_value}$"'

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        if isinstance(value, str) and field == UNMAPPED_FIELD_DEFAULT_NAME:
            return self.contains_modifier(field, value)
        applied_value = self.apply_value(value, value_type=ValueType.regex_value)
        return f'{field} matches "^{applied_value}.*"'

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if field == UNMAPPED_FIELD_DEFAULT_NAME and self.__is_contain_regex_items(value):
            if isinstance(value, str):
                return self.__unmapped_regex_field_to_contains_string(field, value)
            if isinstance(value, list):
                return self.or_token.join(
                    self.__unmapped_regex_field_to_contains_string(field=field, value=v) for v in value
                )
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        if isinstance(value, str) and field == UNMAPPED_FIELD_DEFAULT_NAME:
            return self.contains_modifier(field, value)
        return f'{field} matches "{value}"'

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        if isinstance(value, list):
            rendered_keywords = [f'{UNMAPPED_FIELD_DEFAULT_NAME} CONTAINS "{v}"' for v in value]
            return f"({self.or_token.join(rendered_keywords)})"
        return f'{UNMAPPED_FIELD_DEFAULT_NAME} CONTAINS "{value}"'

    # lrTODO: proper place for these, time constraints cheating and using them in siem_rules
    # def generate_filter(self, field: str, field_type: str, val) -> str:
    #     '''
    #         Most API returns under filter type in their own json field as shown below individually
    #     '''
    #     print(f'Field passing>{field} ({field_type}) Val {type(val)}= {val}')
    #     f_n = self.field_translation(field)
    #     f_t = self.pull_filter_item(f_n, field_type)
    #     filter_structure = {
    #         "filterItemType": 0, 
    #         "fieldOperator": 0, 
    #         "filterMode": 2, 
    #         "filterType": f_t[0],
    #         "values": [
    #             {
    #                 "filterType": f_t[0],
    #                 "valueType": f_t[1],
    #                 "value": val,
    #                 "displayValue": "blank"
    #                 }
    #         ],
    #         "name": f_n
    #     }
    #     return filter_structure 
    #     # return json.dumps(filter_structure, indent=4)

    # def field_translation(self, field):
    #     if field == 'origin.account.name':
    #         field = 'User (Origin)'
    #     elif field == 'general_information.raw_message':
    #         field = 'Message'
    #     elif field in { 'object.process.command_line', 
    #                     'object.script.command_line'
    #                     }:
    #         field = 'Command'
    #     elif field in { 'object.registry_object.path', 
    #                    'object.registry_object.key', 
    #                    'object.resource.name'
    #                    }:
    #         field = 'Object'
    #     elif field in { 'target.host.ip_address.value',
    #                    'target.host.ip_address.value'
    #                    }:
    #         field = 'Address'
    #     elif field in { 'target.host.name',
    #                    'target.host.domain'
    #                    }:
    #         field = 'DHost'
    #     elif field in { 'action.network.byte_information.received',
    #                    'action.network.byte_information.received'
    #                    }:
    #         field = 'BytesIn'
    #     elif field == 'unattributed.host.mac_address':
    #         field = 'MAC'
    #     elif field == 'action.network.http_method':
    #         field = 'SIP'
    #     elif field in { 'origin.url.path', 
    #                    'action.dns.query'
    #                    }:
    #         field = 'URL'
    #     elif field == 'origin.host.domain':
    #         field = 'SHostName'
    #     elif field == 'target.host.domain':
    #         field = 'Host'
    #     elif field == 'action.network.byte_information.sent':
    #         field = 'BytesOut'
    #     elif field == 'action.network.byte_information.total':
    #         field = 'BytesInOut'
    #     elif field == 'object.process.name':
    #         field = 'Application'
    #     elif field == 'action.duration':
    #         field = 'Duration'
    #     elif field == 'process.parent_process.path':
    #         field = 'ParentProcessPath'
    #     elif field == 'object.process.parent_process.name':
    #         field = 'ParentProcessName'
    #     elif field == 'object.file.name' or field == 'TargetFilename':
    #         field = 'Object'
    #     elif field == 'target.host.network_port.value':
    #         field = 'Port'
    #     return field
    

    # def pull_filter_item(self, f_type, f_v):
    #     if f_type == 'User (Origin)':
    #         f_type = 'Login'
        
    #     filter_type = {
    #         'IDMGroupForAccount': 53,
    #         'Address': 44,
    #         'Amount': 64,
    #         'Application': 97,
    #         'MsgClass': 10,
    #         'Command': 112,
    #         'CommonEvent': 11,
    #         'Direction': 2,
    #         'Duration': 62,
    #         'Group': 38,
    #         'BytesIn': 58,
    #         'BytesOut': 59,
    #         'BytesInOut': 95,
    #         'DHost': 100,
    #         'Host': 98,
    #         'SHost': 99,
    #         'ItemsIn': 60,
    #         'ItemsOut': 61,
    #         'ItemsInOut': 96,
    #         'DHostName': 25,
    #         'HostName': 23,
    #         'SHostName': 24,
    #         'KnownService': 16,
    #         'DInterface': 108,
    #         'Interface': 133,
    #         'SInterface': 107,
    #         'DIP': 19,
    #         'IP': 17,
    #         'SIP': 18,
    #         'DIPRange': 22,
    #         'IPRange': 20,
    #         'SIPRange': 21,
    #         'KnownDHost': 15,
    #         'KnownHost': 13,
    #         'KnownSHost': 14,
    #         'Location': 87,
    #         'SLocation': 85,
    #         'DLocation': 86,
    #         'MsgSource': 7,
    #         'Entity': 6,
    #         'RootEntity': 136,
    #         'MsgSourceType': 9,
    #         'DMAC': 104,
    #         'MAC': 132,
    #         'SMAC': 103,
    #         'Message': 35,
    #         'MPERule': 12,
    #         'DNATIP': 106,
    #         'NATIP': 126,
    #         'SNATIP': 105,
    #         'DNATIPRange': 125,
    #         'NATIPRange': 127,
    #         'SNATIPRange': 124,
    #         'DNATPort': 115,
    #         'NATPort': 130,
    #         'SNATPort': 114,
    #         'DNATPortRange': 129,
    #         'NATPortRange': 131,
    #         'SNATPortRange': 128,
    #         'DNetwork': 50,
    #         'Network': 51,
    #         'SNetwork': 49,
    #         'Object': 34,
    #         'ObjectName': 113,
    #         'Login': 29,
    #         'IDMGroupForLogin': 52,
    #         'Priority': 3,
    #         'Process': 41,
    #         'PID': 109,
    #         'Protocol': 28,
    #         'Quantity': 63,
    #         'Rate': 65,
    #         'Recipient': 32,
    #         'Sender': 31,
    #         'Session': 40,
    #         'Severity': 110,
    #         'Size': 66,
    #         'Subject': 33,
    #         'DPort': 27,
    #         'Port': 45,
    #         'SPort': 26,
    #         'DPortRange': 47,
    #         'PortRange': 48,
    #         'SPortRange': 46,
    #         'URL': 42,
    #         'Account': 30,
    #         'User': 43,
    #         'IDMGroupForUser': 54,
    #         'VendorMsgID': 37,
    #         'Version': 111,
    #         'SZone': 93,
    #         'DZone': 94,
    #         'FilterGroup': 1000,
    #         'PolyListItem': 1001,
    #         'Domain': 39,
    #         'DomainOrigin': 137,
    #         'Hash': 138,
    #         'Policy': 139,
    #         'VendorInfo': 140,
    #         'Result': 141,
    #         'ObjectType': 142,
    #         'CVE': 143,
    #         'UserAgent': 144,
    #         'ParentProcessId': 145,
    #         'ParentProcessName': 146,
    #         'ParentProcessPath': 147,
    #         'SerialNumber': 148,
    #         'Reason': 149,
    #         'Status': 150,
    #         'ThreatId': 151,
    #         'ThreatName': 152,
    #         'SessionType': 153,
    #         'Action': 154,
    #         'ResponseCode': 155,
    #         'UserOriginIdentityID': 167,
    #         'Identity': 160,
    #         'UserImpactedIdentityID': 168,
    #         'SenderIdentityID': 169,
    #         'RecipientIdentityID': 170
    #         }

    #     value_type = {
    #     'Byte': 0,
    #     'Int16': 1,
    #     'Int32': 2,
    #     'Int64': 3,
    #     'String': 4,
    #     'IPAddress': 5,
    #     'IPAddressrange': 6,
    #     'TimeOfDay': 7,
    #     'DateRange': 8,
    #     'PortRange': 9,
    #     'Quantity': 10,
    #     'ListReference': 11,
    #     'ListSet': 12,
    #     'Null': 13,
    #     'INVALID': 99
    #     }
    #     return_value = []
    #     if f_type in filter_type:
    #         r_f = filter_type[f_type]
    #     else:
    #         print(f'filterType name reference was not found: {f_type}')
    #         r_f = 0000
    #     if f_v in value_type:
    #         r_v = value_type[f_v]
    #     else:
    #         print(f'filterType name reference was not found: {f_v}')
    #         r_v = 13
    #     return_value.append(r_f)
    #     return_value.append(r_v)
    #     # v_t = value_type[v_type]
    #     return return_value


@render_manager.register
class LogRhythmSiemQueryRender(PlatformQueryRender):
    details: PlatformDetails = logrhythm_siem_rule_details

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = LogRhythmSiemFieldValue(or_token=or_token)
    query_pattern = "{prefix} AND {query}"

    mappings: LogRhythmSiemMappings = logrhythm_siem_mappings
    comment_symbol = "//"
    is_single_line_comment = True
    is_strict_mapping = True

    # def generate(self):
    #     print('moo')

    def generate_prefix(self, log_source_signature: LogSourceSignature, functions_prefix: str = "") -> str:  # noqa: ARG002
        return str(log_source_signature)

    def apply_token(self, token: Union[FieldValue, Keyword, Identifier], source_mapping: SourceMapping) -> str:
        if isinstance(token, FieldValue):
            try:
                mapped_fields = self.map_field(token.field, source_mapping)
            except StrictPlatformException:
                try:
                    return self.field_value_map.apply_field_value(
                        field=UNMAPPED_FIELD_DEFAULT_NAME, operator=token.operator, value=token.value
                    )
                except LogRhythmRegexRenderException as exc:
                    raise LogRhythmRegexRenderException(
                        f"Uncoder does not support complex regexp for unmapped field:"
                        f" {token.field.source_name} for LogRhythm Siem"
                    ) from exc
            if len(mapped_fields) > 1:
                return self.group_token % self.operator_map[LogicalOperatorType.OR].join(
                    [
                        self.field_value_map.apply_field_value(field=field, operator=token.operator, value=token.value)
                        for field in mapped_fields
                    ]
                )
            return self.field_value_map.apply_field_value(
                field=mapped_fields[0], operator=token.operator, value=token.value
            )

        return super().apply_token(token, source_mapping)

    def _generate_from_tokenized_query_container(self, query_container: TokenizedQueryContainer) -> str:
        queries_map = {}
        source_mappings = self._get_source_mappings(query_container.meta_info.source_mapping_ids)

        for source_mapping in source_mappings:
            prefix = self.generate_prefix(source_mapping.log_source_signature)
            if "product" in query_container.meta_info.parsed_logsources:
                prefix = f"{prefix} CONTAINS {query_container.meta_info.parsed_logsources['product'][0]}"
            else:
                prefix = f"{prefix} CONTAINS anything"

            result = self.generate_query(tokens=query_container.tokens, source_mapping=source_mapping)
            rendered_functions = self.generate_functions(query_container.functions.functions, source_mapping)
            not_supported_functions = query_container.functions.not_supported + rendered_functions.not_supported
            finalized_query = self.finalize_query(
                prefix=prefix,
                query=result,
                functions=rendered_functions.rendered,
                not_supported_functions=not_supported_functions,
                meta_info=query_container.meta_info,
                source_mapping=source_mapping,
            )
            if return_only_first_query_ctx_var.get() is True:
                return finalized_query
            queries_map[source_mapping.source_id] = finalized_query

        return self.finalize(queries_map)
