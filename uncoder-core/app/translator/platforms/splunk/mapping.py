from typing import ClassVar, Optional

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature
from app.translator.platforms.splunk.const import splunk_alert_details, splunk_query_details


class SplunkLogSourceSignature(LogSourceSignature):
    def __init__(
        self,
        sources: Optional[list[str]],
        source_types: Optional[list[str]],
        source_categories: Optional[list[str]],
        indices: Optional[list[str]],
        default_source: Optional[dict] = None,
    ):
        self.sources = set(sources or [])
        self.source_types = set(source_types or [])
        self.source_categories = set(source_categories or [])
        self.indices = set(indices or [])
        self._default_source = default_source or {}

    def is_suitable(
        self,
        source: Optional[list[str]] = None,
        sourcetype: Optional[list[str]] = None,
        sourcecategory: Optional[list[str]] = None,
        index: Optional[list[str]] = None,
    ) -> bool:
        conditions = [
            set(source).issubset(self.sources) if source else None,
            set(sourcetype).issubset(self.source_types) if sourcetype else None,
            set(sourcecategory).issubset(self.source_categories) if sourcecategory else None,
            set(index).issubset(self.indices) if index else None,
        ]
        return self._check_conditions(conditions)

    def __str__(self) -> str:
        return " AND ".join((f"{key}={value}" for key, value in self._default_source.items() if value))


class SplunkMappings(BasePlatformMappings):
    global_alternative_mappings: ClassVar[list[str]] = ["ocsf"]

    def prepare_log_source_signature(self, mapping: dict) -> SplunkLogSourceSignature:
        log_source = mapping.get("log_source", {})
        default_log_source = (
            mapping.get("default_log_source") if mapping.get("default_log_source") else {"source": "WinEventLog: *"}
        )
        return SplunkLogSourceSignature(
            sources=log_source.get("source"),
            source_types=log_source.get("sourcetype"),
            source_categories=log_source.get("sourcecategory"),
            indices=log_source.get("index"),
            default_source=default_log_source,
        )


splunk_query_mappings = SplunkMappings(platform_dir="splunk", platform_details=splunk_query_details)
splunk_alert_mappings = SplunkMappings(platform_dir="splunk", platform_details=splunk_alert_details)
