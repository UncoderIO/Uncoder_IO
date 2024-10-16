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
from app.translator.platforms.palo_alto.const import cortex_xsiam_xql_query_details
from app.translator.platforms.palo_alto.functions import cortex_xsiam_xql_functions
from app.translator.platforms.palo_alto.mapping import CortexXSIAMXQLMappings, cortex_xsiam_xql_query_mappings
from app.translator.platforms.palo_alto.renders.base import CortexXQLFieldValueRender, CortexXQLQueryRender


class CortexXSIAMXQLFieldValueRender(CortexXQLFieldValueRender):
    details: PlatformDetails = cortex_xsiam_xql_query_details


@render_manager.register
class CortexXSIAMXQLQueryRender(CortexXQLQueryRender):
    details: PlatformDetails = cortex_xsiam_xql_query_details
    mappings: CortexXSIAMXQLMappings = cortex_xsiam_xql_query_mappings

    field_value_render = CortexXSIAMXQLFieldValueRender(CortexXQLQueryRender.or_token)

    def init_platform_functions(self) -> None:
        self.platform_functions = cortex_xsiam_xql_functions
        self.platform_functions.platform_query_render = self
