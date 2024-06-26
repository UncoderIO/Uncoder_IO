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

from typing import ClassVar

from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render_cti import RenderCTI
from app.translator.managers import render_cti_manager
from app.translator.platforms.microsoft.const import microsoft_defender_details
from app.translator.platforms.microsoft.mappings.mdatp_cti import DEFAULT_MICROSOFT_DEFENDER_MAPPING


@render_cti_manager.register
class MicrosoftDefenderCTI(RenderCTI):
    details: PlatformDetails = microsoft_defender_details

    field_value_templates_map: ClassVar[dict[str, str]] = {
        "default": '{key} =~ "{value}"',
        "url": '{key} has "{value}"',
    }
    or_operator: str = " or "
    group_or_operator: str = " or "
    or_group: str = "({or_group})"
    result_join: str = ""
    final_result_for_many: str = "union * | where ({result})\n"
    final_result_for_one: str = "union * | where {result}\n"
    default_mapping = DEFAULT_MICROSOFT_DEFENDER_MAPPING

    def create_field_value(self, field: str, value: str, generic_field: str) -> str:
        if field_value_template := self.field_value_templates_map.get(generic_field):
            return field_value_template.format(key=field, value=value)
        return self.field_value_templates_map["default"].format(key=field, value=value)
