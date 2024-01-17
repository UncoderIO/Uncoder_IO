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
from app.translator.platforms.microsoft.const import microsoft_defender_details
from app.translator.platforms.microsoft.functions import MicrosoftFunctions, microsoft_defender_functions
from app.translator.platforms.microsoft.mapping import MicrosoftDefenderMappings, microsoft_defender_mappings
from app.translator.platforms.microsoft.renders.microsoft_sentinel import (
    MicrosoftSentinelFieldValue,
    MicrosoftSentinelQueryRender,
)


class MicrosoftDefenderFieldValue(MicrosoftSentinelFieldValue):
    details: PlatformDetails = microsoft_defender_details


class MicrosoftDefenderQueryRender(MicrosoftSentinelQueryRender):
    mappings: MicrosoftDefenderMappings = microsoft_defender_mappings
    details: PlatformDetails = microsoft_defender_details
    platform_functions: MicrosoftFunctions = microsoft_defender_functions
    or_token = "or"
    field_value_map = MicrosoftDefenderFieldValue(or_token=or_token)

    is_strict_mapping = True
