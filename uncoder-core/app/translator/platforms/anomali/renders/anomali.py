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
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import PlatformQueryRender
from app.translator.managers import render_manager
from app.translator.platforms.anomali.const import anomali_query_details
from app.translator.platforms.anomali.mapping import AnomaliMappings, anomali_query_mappings
from app.translator.platforms.base.sql.renders.sql import SqlFieldValueRender


class AnomaliFieldValueRender(SqlFieldValueRender):
    details: PlatformDetails = anomali_query_details

    def keywords(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        return f'message contains "{self._pre_process_value(field, value)}"'


@render_manager.register
class AnomaliQueryRender(PlatformQueryRender):
    details: PlatformDetails = anomali_query_details
    mappings: AnomaliMappings = anomali_query_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    comment_symbol = "--"
    is_single_line_comment = True

    field_value_render = AnomaliFieldValueRender(or_token=or_token)

    @staticmethod
    def _finalize_search_query(query: str) -> str:
        return f"| where {query}" if query else ""
