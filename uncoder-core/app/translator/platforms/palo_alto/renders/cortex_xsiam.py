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

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.exceptions.render import UnsupportedRenderMethod
from app.translator.core.mapping import LogSourceSignature
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseQueryFieldValue, PlatformQueryRender
from app.translator.managers import render_manager
from app.translator.platforms.palo_alto.const import cortex_xql_query_details
from app.translator.platforms.palo_alto.escape_manager import cortex_xql_escape_manager
from app.translator.platforms.palo_alto.mapping import cortex_xsiam_mappings, CortexXSIAMMappings


class CortexXSIAMFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = cortex_xql_query_details
    escape_manager = cortex_xql_escape_manager

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = ", ".join(f'"{v}"' for v in value)
            return f'{field} in ("{values}")'
        elif isinstance(value, int):
            return f'{field} = {value}'
        return f'{field} = "{value}"'

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field} < {value}'

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field} <= {value}'

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field} > {value}'

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{field} >= {value}'

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        return f'{field} != "{value}"'

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f'{field} contains "{value}"'

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=self.apply_value(v)) for v in value)})"
        return f'{field} ~= ".*{self.apply_value(value)}"'

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=self.apply_value(v)) for v in value)})"
        return f'{field} ~= "{self.apply_value(value)}.*"'

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=self.apply_value(v)) for v in value)})"
        return f'{field} ~= "{self.apply_value(value)}"'

    def is_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        if isinstance(value, list):
            return f"({self.or_token.join(self.is_none(field=field, value=v) for v in value)})"
        return f'{field} = null'

    def is_not_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        if isinstance(value, list):
            return f"({self.or_token.join(self.is_not_none(field=field, value=v) for v in value)})"
        return f'{field} != null'

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:  # noqa: ARG002
        raise UnsupportedRenderMethod(platform_name=self.details.name, method="Keywords")


@render_manager.register
class CortexXQLQueryRender(PlatformQueryRender):
    details: PlatformDetails = cortex_xql_query_details
    mappings: CortexXSIAMMappings = cortex_xsiam_mappings

    or_token = "or"
    and_token = "and"
    not_token = "not"

    field_value_map = CortexXSIAMFieldValue(or_token=or_token)
    query_pattern = "{prefix} | filter {query} {functions}"
    comment_symbol = "//"
    is_multi_line_comment = False

    def generate_prefix(self, log_source_signature: LogSourceSignature) -> str:
        preset = f"preset = {log_source_signature.preset}" if log_source_signature.preset else None
        dataset = f"dataset = {log_source_signature.dataset}" if log_source_signature.dataset else None
        return preset or dataset or "datamodel"
