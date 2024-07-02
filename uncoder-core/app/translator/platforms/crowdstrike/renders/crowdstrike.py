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
from app.translator.platforms.base.spl.renders.spl import SplFieldValueRender, SplQueryRender
from app.translator.platforms.crowdstrike.const import crowdstrike_query_details
from app.translator.platforms.crowdstrike.functions import CrowdStrikeFunctions, crowd_strike_functions
from app.translator.platforms.crowdstrike.mapping import CrowdstrikeMappings, crowdstrike_mappings


class CrowdStrikeFieldValueRender(SplFieldValueRender):
    details = crowdstrike_query_details


@render_manager.register
class CrowdStrikeQueryRender(SplQueryRender):
    details: PlatformDetails = crowdstrike_query_details
    mappings: CrowdstrikeMappings = crowdstrike_mappings
    platform_functions: CrowdStrikeFunctions = None

    or_token = "OR"
    field_value_render = CrowdStrikeFieldValueRender(or_token=or_token)
    comment_symbol = "`"

    def init_platform_functions(self) -> None:
        self.platform_functions = crowd_strike_functions
        self.platform_functions.platform_query_render = self
