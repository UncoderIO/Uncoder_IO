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
from typing import Union

from app.converter.platforms.logscale.const import logscale_query_details
from app.converter.platforms.logscale.mapping import LogScaleMappings, logscale_mappings
from app.converter.core.mapping import SourceMapping
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.models.parser_output import MetaInfoContainer
from app.converter.core.render import BaseQueryRender, BaseQueryFieldValue


class LogScaleFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = logscale_query_details

    def apply_value(self, value: Union[str, int]):
        if isinstance(value, str) and '"' in value:
            value = value.translate(str.maketrans({'"':  r'\"'}))
        return value

    def equal_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.equal_modifier(field=field, value=v) for v in value)})"
        return f'{field}="{self.apply_value(value)}"'

    def contains_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f'{field}="*{self.apply_value(value)}*"'

    def endswith_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f'{field}="*{self.apply_value(value)}"'

    def startswith_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f'{field}="{self.apply_value(value)}*"'

    def regex_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f'{field}="/{self.apply_value(value)}/"'

    def keywords(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f'"{self.apply_value(value)}"'


class LogScaleQueryRender(BaseQueryRender):
    details: PlatformDetails = logscale_query_details
    mappings: LogScaleMappings = logscale_mappings

    or_token = "or"
    and_token = ""
    not_token = "not"

    field_value_map = LogScaleFieldValue(or_token=or_token)
    query_pattern = "{prefix} and {query} {functions}"

    def wrap_with_comment(self, value: str) -> str:
        return f"/* {value} */"

    def generate_prefix(self, logsource: dict):
        return ""

    def generate_functions(self, functions: list):
        if not functions:
            return ""

    def finalize_query(self, prefix: str, query: str, functions: str, meta_info: MetaInfoContainer,
                       source_mapping: SourceMapping = None, not_supported_functions: list = None) -> str:
        if prefix:
            query = self.query_pattern.format(prefix=prefix, query=query, functions=functions)
        else:
            query = f'{query} {functions}'
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return query + rendered_not_supported
        return query
