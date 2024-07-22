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
import math
from datetime import timedelta
from typing import Optional

import yaml

from app.translator.core.context_vars import wrap_query_with_meta_info_ctx_var
from app.translator.core.exceptions.render import BaseRenderException
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import RawQueryContainer, TokenizedQueryContainer
from app.translator.core.render import QueryRender
from app.translator.managers import RenderManager, render_manager
from app.translator.platforms.microsoft.const import MICROSOFT_SENTINEL_QUERY_DETAILS
from app.translator.platforms.roota.const import ROOTA_RULE_DETAILS, ROOTA_RULE_TEMPLATE
from app.translator.platforms.sigma.const import SIGMA_RULE_DETAILS
from app.translator.platforms.sigma.mapping import sigma_rule_mappings

_AUTOGENERATED_TEMPLATE = "Autogenerated RootA Rule"


@render_manager.register
class RootARender(QueryRender):
    details: PlatformDetails = PlatformDetails(**ROOTA_RULE_DETAILS)
    render_manager: RenderManager = render_manager

    @staticmethod
    def __render_timeframe(timeframe: timedelta) -> str:
        total_seconds = timeframe.total_seconds()

        week_ = 7  # days
        day_ = 24  # hours
        hour_ = 60  # minutes
        minute_ = 60  # seconds

        if total_seconds >= week_ * day_ * hour_ * minute_:
            timeframe_value = math.ceil(total_seconds / (week_ * day_ * hour_ * minute_))
            timeframe_unit = "w"
        elif total_seconds >= day_ * hour_ * minute_:
            timeframe_value = math.ceil(total_seconds / (day_ * hour_ * minute_))
            timeframe_unit = "d"
        elif total_seconds >= hour_ * minute_:
            timeframe_value = math.ceil(total_seconds / (hour_ * minute_))
            timeframe_unit = "h"
        elif total_seconds >= minute_:
            timeframe_value = math.ceil(total_seconds / minute_)
            timeframe_unit = "m"
        else:
            timeframe_value = math.ceil(total_seconds)
            timeframe_unit = "s"
        return f"{timeframe_value}{timeframe_unit}"

    @staticmethod
    def __get_source_mapping(source_mapping_ids: list[str]) -> Optional[SourceMapping]:
        for source_mapping_id in source_mapping_ids:
            if source_mapping := sigma_rule_mappings.get_source_mapping(source_mapping_id):
                return source_mapping

    def generate(
        self, raw_query_container: RawQueryContainer, tokenized_query_container: Optional[TokenizedQueryContainer]
    ) -> str:
        if not tokenized_query_container or not tokenized_query_container.meta_info:
            raise BaseRenderException("Meta info is required")
        logsources = {}
        if raw_query_container.language == SIGMA_RULE_DETAILS["platform_id"]:
            query_language = MICROSOFT_SENTINEL_QUERY_DETAILS["platform_id"]
            source_mapping_ids = tokenized_query_container.meta_info.source_mapping_ids.copy()
            for source_mapping in source_mapping_ids:
                tokenized_query_container.meta_info.source_mapping_ids = [source_mapping]
                wrap_query_with_meta_info_ctx_var.set(False)
                query = self.render_manager.get(query_language).generate(
                    raw_query_container=raw_query_container, tokenized_query_container=tokenized_query_container
                )
                if query:
                    break
            if suitable_sigma_mapping := sigma_rule_mappings.get_source_mapping(source_mapping):
                logsources = suitable_sigma_mapping.log_source_signature.log_sources

        else:
            query_language = raw_query_container.language
            query = raw_query_container.query

        if not logsources and tokenized_query_container.meta_info.parsed_logsources:
            logsources = tokenized_query_container.meta_info.parsed_logsources
        elif suitable_sigma_mapping := sigma_rule_mappings.get_source_mapping(source_mapping):
            logsources = suitable_sigma_mapping.log_source_signature.log_sources

        rule = ROOTA_RULE_TEMPLATE.copy()
        rule["name"] = tokenized_query_container.meta_info.title or _AUTOGENERATED_TEMPLATE
        rule["details"] = tokenized_query_container.meta_info.description or rule["details"]
        rule["author"] = tokenized_query_container.meta_info.author or rule["author"]
        rule["severity"] = tokenized_query_container.meta_info.severity or rule["severity"]
        rule["date"] = tokenized_query_container.meta_info.date
        rule["detection"]["language"] = query_language
        rule["detection"]["body"] = query
        rule["license"] = tokenized_query_container.meta_info.license
        rule["uuid"] = tokenized_query_container.meta_info.id
        rule["references"] = tokenized_query_container.meta_info.references or rule["references"]
        rule["tags"] = tokenized_query_container.meta_info.tags or rule["tags"]

        mitre_attack = tokenized_query_container.meta_info.mitre_attack
        tactics = [tactic["external_id"].lower() for tactic in mitre_attack.get("tactics", [])]
        techniques = [technique["technique_id"].lower() for technique in mitre_attack.get("techniques", [])]
        rule["mitre-attack"] = tactics + techniques

        if tokenized_query_container.meta_info.timeframe:
            rule["correlation"] = {}
            rule["correlation"]["timeframe"] = self.__render_timeframe(tokenized_query_container.meta_info.timeframe)

        if logsources:
            for logsource_type, value in logsources.items():
                rule["logsource"][logsource_type] = value.capitalize()

        return yaml.dump(rule, default_flow_style=False, sort_keys=False, indent=4)
