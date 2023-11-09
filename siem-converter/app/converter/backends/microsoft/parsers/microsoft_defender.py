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

from app.converter.backends.microsoft.const import microsoft_defender_details
from app.converter.backends.microsoft.parsers.microsoft_sentinel import MicrosoftParser
from app.converter.backends.microsoft.mapping import microsoft_defender_mappings, MicrosoftDefenderMappings
from app.converter.core.models.platform_details import PlatformDetails


class MicrosoftDefenderQueryParser(MicrosoftParser):
    mappings: MicrosoftDefenderMappings = microsoft_defender_mappings
    details: PlatformDetails = microsoft_defender_details
