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

from app.translator.core.models.platform_details import PlatformDetails
from app.translator.managers import render_manager
from app.translator.platforms.base.sql.renders.sql import SQLFieldValueRender, SQLQueryRender
from app.translator.platforms.hunters.const import hunters_query_details
from app.translator.platforms.hunters.mapping import HuntersMappings, hunters_query_mappings


class HuntersFieldValueRender(SQLFieldValueRender):
    details: PlatformDetails = hunters_query_details


@render_manager.register
class HuntersQueryRender(SQLQueryRender):
    details: PlatformDetails = hunters_query_details
    mappings: HuntersMappings = hunters_query_mappings

    or_token = "OR"

    field_value_render = HuntersFieldValueRender(or_token=or_token)

    @staticmethod
    def _finalize_search_query(query: str) -> str:
        return f"WHERE {query}" if query else ""
