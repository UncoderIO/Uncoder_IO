from typing import Optional

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature
from app.translator.platforms.logscale.const import logscale_alert_details, logscale_query_details


class LogScaleLogSourceSignature(LogSourceSignature):
    def __init__(self, default_source: Optional[dict] = None):
        self._default_source = default_source or {}

    def __str__(self) -> str:
        return " ".join((f"{key}={value}" for key, value in self._default_source.items() if value))

    def is_suitable(self) -> bool:
        raise True


class LogScaleMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> LogScaleLogSourceSignature:
        default_log_source = mapping.get("default_log_source")
        return LogScaleLogSourceSignature(default_source=default_log_source)


logscale_query_mappings = LogScaleMappings(platform_dir="logscale", platform_details=logscale_query_details)
logscale_alert_mappings = LogScaleMappings(platform_dir="logscale", platform_details=logscale_alert_details)
