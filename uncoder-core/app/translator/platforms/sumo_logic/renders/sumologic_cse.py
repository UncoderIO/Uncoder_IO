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
from app.translator.core.render import PlatformQueryRender

from app.translator.platforms.sumo_logic.const import sumologic_search_query_details
from app.translator.platforms.sumo_logic.mapping import SumoLogicMappings, sumologic_mappings
from app.translator.platforms.sumo_logic.renders.sumologic import SumologicFieldValue



@render_manager.register
class SumologicCSERender(PlatformQueryRender):
    details: PlatformDetails = sumologic_search_query_details
    mappings: SumoLogicMappings = sumologic_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = SumologicFieldValue(or_token=or_token)
    query_pattern = "{prefix} {query} {functions}"


@render_manager.register
class SumologicCSERuleRender(PlatformQueryRender):
    details: PlatformDetails = sumologic_search_query_details
    mappings: SumoLogicMappings = sumologic_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = SumologicFieldValue(or_token=or_token)
    query_pattern = "{prefix} {query} {functions}"