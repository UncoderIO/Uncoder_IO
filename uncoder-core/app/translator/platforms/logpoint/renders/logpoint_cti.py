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
from app.translator.core.render_cti import RenderCTI
from app.translator.platforms.logpoint.const import LOGPOINT_QUERY_DETAILS
from app.translator.platforms.logpoint.mappings.logpoint_cti import DEFAULT_LOGPOINT_MAPPING


class LogpointCTI(RenderCTI):
    details: PlatformDetails = PlatformDetails(**LOGPOINT_QUERY_DETAILS)

    field_value_template: str = '"{value}"'
    or_operator: str = ", "
    group_or_operator: str = " "
    or_group: str = "{processing_key} IN [{or_group}]"
    result_join: str = ""
    final_result_for_many: str = "({result})\n"
    final_result_for_one: str = "{result}\n"
    default_mapping = DEFAULT_LOGPOINT_MAPPING
