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

from app.converter.platforms.carbonblack.const import CARBON_BLACK_QUERY_DETAILS
from app.converter.platforms.carbonblack.mappings.carbonblack_cti import DEFAULT_CARBONBLACK_MAPPING
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.render_cti import RenderCTI


class CarbonBlackCTI(RenderCTI):
    details: PlatformDetails = PlatformDetails(**CARBON_BLACK_QUERY_DETAILS)

    data_map: str = "{key}:{value}"
    or_operator: str = " OR "
    group_or_operator: str = " OR "
    or_group: str = "({or_group})"
    result_join: str = ""
    final_result_for_many: str = "({result})\n"
    final_result_for_one: str = "{result}\n"
    default_mapping = DEFAULT_CARBONBLACK_MAPPING
