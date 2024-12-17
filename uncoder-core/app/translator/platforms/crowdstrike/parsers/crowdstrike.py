"""
Uncoder IO Commercial Edition License
-----------------------------------------------------------------
Copyright (c) 2024 SOC Prime, Inc.

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
from app.translator.managers import parser_manager
from app.translator.platforms.base.spl.parsers.spl import SPLQueryParser
from app.translator.platforms.crowdstrike.const import crowdstrike_query_details
from app.translator.platforms.crowdstrike.functions import CrowdStrikeFunctions, crowd_strike_functions
from app.translator.platforms.crowdstrike.mapping import CrowdstrikeMappings, crowdstrike_query_mappings


@parser_manager.register_supported_by_roota
class CrowdStrikeQueryParser(SPLQueryParser):
    details: PlatformDetails = crowdstrike_query_details

    log_source_pattern = r"___source_type___\s*=\s*(?:\"(?P<d_q_value>[%a-zA-Z_*:0-9\-/]+)\"|(?P<value>[%a-zA-Z_*:0-9\-/]+))(?:\s+(?:and|or)\s+|\s+)?"  # noqa: E501
    log_source_key_types = ("event_simpleName",)

    mappings: CrowdstrikeMappings = crowdstrike_query_mappings
    platform_functions: CrowdStrikeFunctions = crowd_strike_functions

    wrapped_with_comment_pattern = r"^\s*`(?:|\n|.)*`"
