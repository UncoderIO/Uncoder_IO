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
from typing import Union

from app.translator.platforms.base.lucene.renders.lucene import LuceneQueryRender, LuceneFieldValue
from app.translator.platforms.elasticsearch.const import elasticsearch_lucene_query_details
from app.translator.platforms.elasticsearch.mapping import ElasticSearchMappings, elasticsearch_mappings
from app.translator.core.models.platform_details import PlatformDetails


class ElasticSearchFieldValue(LuceneFieldValue):
    details: PlatformDetails = elasticsearch_lucene_query_details

    def apply_value(self, value: Union[str, int]):
        if isinstance(value, int):
            return value
        if " " in value:
            return f'"{value}"'.replace(" ", r"\ ")
        return value


class ElasticSearchQueryRender(LuceneQueryRender):
    details: PlatformDetails = elasticsearch_lucene_query_details
    mappings: ElasticSearchMappings = elasticsearch_mappings

    or_token = "OR"
    field_value_map = ElasticSearchFieldValue(or_token=or_token)
