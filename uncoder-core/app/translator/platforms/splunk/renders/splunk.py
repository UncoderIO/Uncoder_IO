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
from app.translator.platforms.base.spl.renders.spl import SPLFieldValueRender, SPLQueryRender
from app.translator.platforms.splunk.const import splunk_query_details
from app.translator.platforms.splunk.functions import SplunkFunctions, splunk_functions
from app.translator.platforms.splunk.mapping import SplunkMappings, splunk_query_mappings


class SplunkFieldValueRender(SPLFieldValueRender):
    details: PlatformDetails = splunk_query_details


@render_manager.register
class SplunkQueryRender(SPLQueryRender):
    details: PlatformDetails = splunk_query_details
    mappings: SplunkMappings = splunk_query_mappings
    platform_functions: SplunkFunctions = None

    or_token = "OR"

    field_value_render = SplunkFieldValueRender(or_token=or_token)

    def init_platform_functions(self) -> None:
        self.platform_functions = splunk_functions
        self.platform_functions.platform_query_render = self
