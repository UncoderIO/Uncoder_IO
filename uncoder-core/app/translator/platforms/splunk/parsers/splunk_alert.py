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

import re

from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import MetaInfoContainer, RawQueryContainer
from app.translator.platforms.splunk.const import splunk_alert_details
from app.translator.platforms.splunk.parsers.splunk import SplunkQueryParser


class SplunkAlertParser(SplunkQueryParser):
    details: PlatformDetails = splunk_alert_details

    def parse_raw_query(self, text: str, language: str) -> RawQueryContainer:
        query = re.search(r"search\s*=\s*(?P<query>.+)", text).group("query")
        description = re.search(r"description\s*=\s*(?P<description>.+)", text).group("description")
        return RawQueryContainer(query=query, language=language, meta_info=MetaInfoContainer(description=description))
