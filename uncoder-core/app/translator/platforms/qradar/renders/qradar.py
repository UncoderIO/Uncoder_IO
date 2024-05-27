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
from typing import Callable, List, Optional, Union
from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.str_value_manager import StrValue
from app.translator.managers import render_manager
from app.translator.platforms.base.aql.renders.aql import AQLFieldValue, AQLQueryRender
from app.translator.platforms.qradar.const import qradar_query_details


class QradarFieldValue(AQLFieldValue):
    details: PlatformDetails = qradar_query_details

    def _has_wildcards(self, value: str) -> bool:
        return any(item in value for item in ('%', '_'))

    def _render_qradar_modifiers(self, field: str, values: List[Union[int, str, StrValue]], modifier_func: Callable, prefix: Optional[str] = '', suffix: Optional[str] = '') -> str:
        """
            Renders values for a list of inputs, applying the appropriate modifier or regex function.
            
            Args:
                field - str: The database field to modify.
                values - List[Union[int, str, StrValue]]: The list of values to process.
                modifier_fun - Callable: The function to call for non-regex modifications.
                prefix - Optional[str]: The prefix to add to each value for regex. Defaults to ''.
                suffix - Optional[str]: The suffix to add to each value for regex. Defaults to ''.
            
            Returns:
                str: The rendered query part.
        """
        rendered_values = [
            self.regex_modifier(field, f"{prefix}{v}{suffix}") if self._has_wildcards(str(v)) else modifier_func(field, v)
            for v in values
        ]
        return f"({self.or_token.join(rendered_values)})"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return self._render_qradar_modifiers(field, value, super().contains_modifier, prefix=".*")
        if self._has_wildcards(str(value)):
            return self.regex_modifier(field, f".*{value}")
        return f"\"{field}\" ILIKE '%{self._apply_value(value)}'"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return self._render_qradar_modifiers(field, value, super().startswith_modifier, suffix=".*")
        if self._has_wildcards(str(value)):
            return self.regex_modifier(field, f"{value}.*")
        return f"\"{field}\" ILIKE '{self._apply_value(value)}%'"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return self._render_qradar_modifiers(field, value, super().contains_modifier, prefix=".*", suffix=".*")
        if self._has_wildcards(str(value)):
            return self.regex_modifier(field, f".*{value}.*")
        return f"\"{field}\" ILIKE '%{self._apply_value(value)}%'"


@render_manager.register
class QradarQueryRender(AQLQueryRender):

    or_token = "OR"

    field_value_map = QradarFieldValue(or_token=or_token)
    details: PlatformDetails = qradar_query_details
