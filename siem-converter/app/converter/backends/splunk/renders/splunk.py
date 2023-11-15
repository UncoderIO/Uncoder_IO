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

from app.converter.backends.splunk.const import splunk_query_details
from app.converter.backends.splunk.mapping import SplunkMappings, splunk_mappings
from app.converter.core.exceptions.render import UnsupportedRenderMethod
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.render import BaseQueryRender, BaseQueryFieldValue


class SplunkFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = splunk_query_details

    def equal_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"
        return f'{field}="{value}"'

    def contains_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join([self.contains_modifier(field=field, value=v) for v in value])})"
        return f'{field}="*{value}*"'

    def endswith_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join([self.endswith_modifier(field=field, value=v) for v in value])})"
        return f'{field}="*{value}"'

    def startswith_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join([self.startswith_modifier(field=field, value=v) for v in value])})"
        return f'{field}="{value}*"'

    def keywords(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f'"{value}"'

    def regex_modifier(self, field, value):
        raise UnsupportedRenderMethod(platform_name=self.details.name, method="Regex Expression")


class SplunkQueryRender(BaseQueryRender):
    details: PlatformDetails = splunk_query_details

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = SplunkFieldValue(or_token=or_token)
    query_pattern = "{prefix} {query} {functions}"
    comment_symbol = '```'
    mappings: SplunkMappings = splunk_mappings

    def generate_functions(self, functions: list):
        return ""

    def wrap_with_comment(self, value: str) -> str:
        return f"{self.comment_symbol} {value} {self.comment_symbol}"
