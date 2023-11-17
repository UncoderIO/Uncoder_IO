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

from app.converter.platforms.opensearch.const import opensearch_query_details
from app.converter.platforms.opensearch.mappings.opensearch_cti import DEFAULT_OPENSEARCH_MAPPING
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.render_cti import RenderCTI


class OpenSearchCTI(RenderCTI):
    details: PlatformDetails = opensearch_query_details

    data_map: str = '"{value}"'
    or_operator: str = " OR "
    group_or_operator: str = " OR "
    or_group: str = "{processing_key}:({or_group})"
    result_join: str = ""
    final_result_for_many: str = "({result})\n"
    final_result_for_one: str = "{result}\n"
    default_mapping = DEFAULT_OPENSEARCH_MAPPING
