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
from typing import List

from app.translator.core.mapping import SourceMapping
from app.translator.core.models.functions.base import Function
from app.translator.platforms.chronicle.const import chronicle_query_details
from app.translator.platforms.chronicle.mapping import ChronicleMappings, chronicle_mappings
from app.translator.core.exceptions.render import UnsupportedRenderMethod
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseQueryRender, BaseQueryFieldValue


class ChronicleFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = chronicle_query_details

    @staticmethod
    def apply_field(field):
        return field

    def equal_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f'{self.apply_field(field)} = "{value}" nocase'

    def contains_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f'{self.apply_field(field)} = /.*{value}.*/ nocase'

    def endswith_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f'{self.apply_field(field)} = /.*{value}$/ nocase'

    def startswith_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f'{self.apply_field(field)} = /^{value}.*/ nocase'

    def regex_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f'{self.apply_field(field)} = /{value}/ nocase'

    def keywords(self, field, value):
        raise UnsupportedRenderMethod(platform_name=self.details.name, method="Keywords")


class ChronicleQueryRender(BaseQueryRender):
    details: PlatformDetails = chronicle_query_details
    mappings: ChronicleMappings = chronicle_mappings

    is_strict_mapping = True

    or_token = "or"
    and_token = "and"
    not_token = "not"

    field_value_map = ChronicleFieldValue(or_token=or_token)
    query_pattern = "{query} {functions}"
    comment_symbol = r"//"

    def generate_prefix(self, logsource: dict):
        return ""

    def generate_functions(self, functions: List[Function], source_mapping: SourceMapping) -> str:
        return ""
