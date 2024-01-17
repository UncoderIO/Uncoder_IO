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
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.platforms.base.spl.renders.spl import SplFieldValue, SplQueryRender
from app.translator.platforms.splunk.const import splunk_query_details
from app.translator.platforms.splunk.functions import SplunkFunctions, splunk_functions
from app.translator.platforms.splunk.mapping import SplunkMappings, splunk_mappings


class SplunkFieldValue(SplFieldValue):
    details: PlatformDetails = splunk_query_details


class SplunkQueryRender(SplQueryRender):
    details: PlatformDetails = splunk_query_details

    or_token = "OR"

    field_value_map = SplunkFieldValue(or_token=or_token)
    mappings: SplunkMappings = splunk_mappings
    platform_functions: SplunkFunctions = splunk_functions

    def __init__(self):
        super().__init__()
        self.platform_functions.manager.init_search_func_render(self)
