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
from app.translator.platforms.base.lucene.renders.lucene import LuceneFieldValue, LuceneQueryRender
from app.translator.platforms.graylog.const import graylog_details
from app.translator.platforms.graylog.mapping import GraylogMappings, graylog_mappings


class GraylogFieldValue(LuceneFieldValue):
    details: PlatformDetails = graylog_details


class GraylogQueryRender(LuceneQueryRender):
    details: PlatformDetails = graylog_details
    mappings: GraylogMappings = graylog_mappings

    or_token = "OR"
    field_value_map = GraylogFieldValue(or_token=or_token)
