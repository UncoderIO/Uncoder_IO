"""
Uncoder IO Commercial Edition License
-----------------------------------------------------------------
Copyright (c) 2023 SOC Prime, Inc.

This file is part of the Uncoder IO Commercial Edition ("CE") and is
licensed under the Uncoder IO Non-Commercial License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://github.com/UncoderIO/UncoderIO/blob/main/LICENSE

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-----------------------------------------------------------------
"""

from app.translator.core.models.platform_details import PlatformDetails
from app.translator.platforms.microsoft.const import microsoft_defender_details
from app.translator.platforms.microsoft.functions import MicrosoftFunctions, microsoft_defender_functions
from app.translator.platforms.microsoft.mapping import MicrosoftDefenderMappings, microsoft_defender_mappings
from app.translator.platforms.microsoft.parsers.microsoft_sentinel import MicrosoftSentinelQueryParser


class MicrosoftDefenderQueryParser(MicrosoftSentinelQueryParser):
    mappings: MicrosoftDefenderMappings = microsoft_defender_mappings
    details: PlatformDetails = microsoft_defender_details
    platform_functions: MicrosoftFunctions = microsoft_defender_functions
