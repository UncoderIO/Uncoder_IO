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
from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.mapping import LogSourceSignature
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.managers import render_manager
from app.translator.platforms.base.sql.renders.sql import SqlFieldValue, SqlQueryRender
from app.translator.platforms.elasticsearch.mapping import ElasticSearchMappings, elasticsearch_mappings
from app.translator.platforms.elasticsearch.const import elasticsearch_esql_query_details


class ESQLFieldValue(SqlFieldValue):
    details: PlatformDetails = elasticsearch_esql_query_details

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f'{field} LIKE "*{value}*"'

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f'{field} LIKE "*{value}?"'

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f'{field} LIKE "{value}%"'

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f'{field} RLIKE "{value}"'


@render_manager.register
class ESQLQueryRender(SqlQueryRender):
    details: PlatformDetails = elasticsearch_esql_query_details
    mappings: ElasticSearchMappings = elasticsearch_mappings

    or_token = "OR"
    field_value_map = ESQLFieldValue(or_token=or_token)

    def generate_prefix(self, log_source_signature: LogSourceSignature, functions_prefix: str = "") -> str:  # noqa: ARG002
        table = str(log_source_signature) if str(log_source_signature) else "*"
        return f"FROM {table} metadata _id, _version, _index |"