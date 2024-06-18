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

from typing import Optional, Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer
from app.translator.core.render import BaseQueryFieldValue, PlatformQueryRender
from app.translator.managers import render_manager
from app.translator.platforms.logscale.const import logscale_query_details
from app.translator.platforms.logscale.escape_manager import logscale_escape_manager
from app.translator.platforms.logscale.functions import LogScaleFunctions, log_scale_functions
from app.translator.platforms.logscale.mapping import LogScaleMappings, logscale_mappings


class LogScaleFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = logscale_query_details
    escape_manager = logscale_escape_manager

    def apply_field_name(self, field_name: str) -> str:
        if not field_name.isalpha():
            return f'"{field_name}"'
        return field_name

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.equal_modifier(field=field, value=v) for v in value)})"
        if value == "":
            return f'{self.apply_field_name(field_name=field)}=""'
        if value == "*":
            return f"{self.apply_field_name(field_name=field)}=/^/i"
        return f"{self.apply_field_name(field_name=field)}=/{self.apply_value(value)}/i"

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{self.apply_field_name(field_name=field)}<"{self.apply_value(value)}"'

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{self.apply_field_name(field_name=field)}<="{self.apply_value(value)}"'

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{self.apply_field_name(field_name=field)}>"{self.apply_value(value)}"'

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{self.apply_field_name(field_name=field)}>="{self.apply_value(value)}"'

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        return f"{self.apply_field_name(field_name=field)}!=/{self.apply_value(value)}/i"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f"{self.apply_field_name(field_name=field)}=/{self.apply_value(value)}/i"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f"{self.apply_field_name(field_name=field)}=/{self.apply_value(value)}$/i"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f"{self.apply_field_name(field_name=field)}=/^{self.apply_value(value)}/i"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f"{self.apply_field_name(field_name=field)}=/{self.apply_value(value)}/"

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.keywords(field=field, value=v) for v in value)})"
        return f"/{self.apply_value(value)}/i"


@render_manager.register
class LogScaleQueryRender(PlatformQueryRender):
    details: PlatformDetails = logscale_query_details
    mappings: LogScaleMappings = logscale_mappings
    platform_functions: LogScaleFunctions = None

    or_token = "or"
    and_token = ""
    not_token = "not"

    field_value_map = LogScaleFieldValue(or_token=or_token)
    query_pattern = "{prefix} {query} {functions}"

    def init_platform_functions(self) -> None:
        self.platform_functions = log_scale_functions
        self.platform_functions.platform_query_render = self

    def wrap_with_comment(self, value: str) -> str:
        return f"/* {value} */"

    def finalize_query(
        self,
        prefix: str,
        query: str,
        functions: str,
        meta_info: Optional[MetaInfoContainer] = None,
        source_mapping: Optional[SourceMapping] = None,  # noqa: ARG002
        not_supported_functions: Optional[list] = None,
        *args,  # noqa: ARG002
        **kwargs,  # noqa: ARG002
    ) -> str:
        if prefix:
            query = self.query_pattern.format(prefix=prefix, query=query, functions=functions)
        else:
            query = f"{query} {functions.lstrip()}"
        query = self.wrap_query_with_meta_info(meta_info=meta_info, query=query)
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return query + rendered_not_supported
        return query
