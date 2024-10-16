from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature
from app.translator.platforms.hunters.const import hunters_query_details


class HuntersLogSourceSignature(LogSourceSignature):
    def __init__(self, default_source: dict):
        self._default_source = default_source or {}

    def is_suitable(self) -> bool:
        return True

    def __str__(self) -> str:
        return self._default_source.get("table", "")


class HuntersMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> HuntersLogSourceSignature:
        default_log_source = mapping["default_log_source"]
        return HuntersLogSourceSignature(default_source=default_log_source)


hunters_query_mappings = HuntersMappings(platform_dir="hunters", platform_details=hunters_query_details)
