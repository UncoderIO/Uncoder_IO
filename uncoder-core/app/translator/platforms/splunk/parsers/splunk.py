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
from app.translator.platforms.base.spl.parsers.spl import SplQueryParser
from app.translator.platforms.splunk.const import splunk_query_details
from app.translator.platforms.splunk.functions import SplunkFunctions, splunk_functions
from app.translator.platforms.splunk.mapping import SplunkMappings, splunk_query_mappings


@parser_manager.register_supported_by_roota
class SplunkQueryParser(SplQueryParser):
    details: PlatformDetails = splunk_query_details
    mappings: SplunkMappings = splunk_query_mappings
    platform_functions: SplunkFunctions = splunk_functions

    log_source_pattern = r"^___source_type___\s*=\s*(?:\"(?P<d_q_value>[%a-zA-Z_*:0-9\-/]+)\"|(?P<value>[%a-zA-Z_*:0-9\-/]+))(?:\s+(?:and|or)\s+|\s+)?"  # noqa: E501
    log_source_key_types = ("index", "source", "sourcetype", "sourcecategory")
