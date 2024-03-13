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
from app.translator.core.render_cti import RenderCTI
from app.translator.platforms.microsoft.const import microsoft_sentinel_query_details
from app.translator.platforms.microsoft.mappings.microsoft_sentinel_cti import DEFAULT_MICROSOFT_SENTINEL_MAPPING


class MicrosoftSentinelCTI(RenderCTI):
    details: PlatformDetails = microsoft_sentinel_query_details

    field_value_template: str = '@"{value}"'
    or_operator: str = " or "
    group_or_operator: str = " or "
    or_group: str = "({or_group})"
    result_join: str = ""
    final_result_for_many: str = "search ({result})\n"
    final_result_for_one: str = "search {result}\n"
    default_mapping = DEFAULT_MICROSOFT_SENTINEL_MAPPING
