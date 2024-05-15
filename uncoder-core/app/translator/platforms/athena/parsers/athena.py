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
from app.translator.platforms.athena.const import athena_details
from app.translator.platforms.athena.mapping import AthenaMappings, athena_mappings
from app.translator.platforms.base.sql.parsers.sql import SqlQueryParser


@parser_manager.register_supported_by_roota
class AthenaQueryParser(SqlQueryParser):
    details: PlatformDetails = athena_details
    mappings: AthenaMappings = athena_mappings
    query_delimiter_pattern = r"\sFROM\s\S*\sWHERE\s"
    table_pattern = r"\sFROM\s(?P<table>[a-zA-Z\.\-\*]+)\sWHERE\s"
