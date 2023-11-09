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

from app.converter.backends.microsoft.const import microsoft_sentinel_query_details
from app.converter.backends.microsoft.mapping import MicrosoftSentinelMappings, microsoft_sentinel_mappings
from app.converter.core.mapping import LogSourceSignature
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.render import BaseQueryRender, BaseQueryFieldValue
from app.converter.backends.microsoft.siem_functions.base import MicroSoftQueryFunctions


class MicrosoftSentinelFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = microsoft_sentinel_query_details

    def equal_modifier(self, field, value):
        if isinstance(value, str):
            return f"{field} =~ @'{value}'"
        elif isinstance(value, list):
            prepared_values = ", ".join(f"@'{v}'" for v in value)
            operator = "in~" if all(isinstance(v, str) for v in value) else "in"
            return f'{field} {operator} ({prepared_values})'
        return f'{field} == {value}'

    def contains_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f"{field} contains @'{value}'"

    def endswith_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f"{field} endswith @'{value}'"

    def startswith_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f"{field} startswith @'{value}'"

    def __regex_modifier(self, field, value):
        return f"{field} matches regex @'(?i){value}'"

    def regex_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.__regex_modifier(field=field, value=v) for v in value)})"
        return f'({self.__regex_modifier(field=field, value=value)})'

    def keywords(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f"* contains @'{value}'"


class MicrosoftSentinelQueryRender(BaseQueryRender):
    details: PlatformDetails = microsoft_sentinel_query_details

    or_token = "or"
    and_token = "and"
    not_token = "not"

    field_value_map = MicrosoftSentinelFieldValue(or_token=or_token)
    query_pattern = "{prefix} | where {query} {functions}"

    mappings: MicrosoftSentinelMappings = microsoft_sentinel_mappings
    comment_symbol = "//"

    def generate_prefix(self, log_source_signature: LogSourceSignature) -> str:
        return str(log_source_signature)

    def render_not_supported_functions(self, not_supported_functions: list) -> str:
        render_not_suported = "\n".join([f'// {i}' for i in not_supported_functions])
        return "\n\n" + f"// {self.unsupported_functions_text}" + render_not_suported

    def generate_functions(self, functions: list) -> str:
        if not functions:
            return ""
        result = MicroSoftQueryFunctions().render(functions)
        return result
