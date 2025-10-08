"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2024 SOC Prime, Inc.

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

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.platforms.exabeam.const import (
    exabeam_analytics_rule_details,
    exabeam_correlation_rule_details,
    exabeam_eql_query_details,
)


class ExabeamLogSourceSignature(LogSourceSignature):
    def __init__(self, default_source: dict, log_sources: dict):
        self._default_source = default_source
        self.log_sources = log_sources

    def is_suitable(self, log_source_signature: dict) -> bool:
        for log_source_key, log_source_value in log_source_signature.items():
            if log_source_key in self.log_sources:
                log_source_values = self.log_sources[log_source_key]
                if isinstance(log_source_values, list):
                    if log_source_value in log_source_values:
                        return True
                elif log_source_values == log_source_value:
                    return True
        return False

    def __str__(self) -> str:
        return self._default_source.get("activity_type", "")


class ExabeamMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> ExabeamLogSourceSignature:
        default_source = mapping.get("default_log_source", {})
        log_sources = mapping.get("log_source", {})
        return ExabeamLogSourceSignature(default_source=default_source, log_sources=log_sources)
    
    @property
    def source_mappings(self):
        return self._source_mappings


# Mapping instances are created inline in render classes to avoid circular imports