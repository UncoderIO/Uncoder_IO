from app.translator.core.mapping import BaseStrictLogSourcesPlatformMappings, LogSourceSignature
from app.translator.platforms.sentinel_one.const import sentinel_one_power_query_details


class SentinelOnePowerQueryLogSourceSignature(LogSourceSignature):
    def is_suitable(self) -> bool:
        return True

    def __str__(self) -> str:
        return ""


class SentinelOnePowerQueryMappings(BaseStrictLogSourcesPlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> SentinelOnePowerQueryLogSourceSignature:
        ...


sentinel_one_power_query_query_mappings = SentinelOnePowerQueryMappings(
    platform_dir="sentinel_one", platform_details=sentinel_one_power_query_details
)
