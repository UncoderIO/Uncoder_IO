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
from app.translator.managers import render_cti_manager
from app.translator.platforms.exabeam.const import DEFAULT_EXABEAM_CTI_MAPPING, exabeam_eql_query_details


@render_cti_manager.register
class ExabeamCTI(RenderCTI):
    details: PlatformDetails = exabeam_eql_query_details

    field_value_template: str = '{key} = "{value}"'
    or_operator: str = " OR "
    group_or_operator: str = " OR "
    or_group: str = "({or_group})"
    result_join: str = ""
    final_result_for_many: str = "SELECT * WHERE ({result})"
    final_result_for_one: str = "SELECT * WHERE {result}"
    default_mapping = DEFAULT_EXABEAM_CTI_MAPPING