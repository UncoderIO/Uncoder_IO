from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature
from app.translator.platforms.carbonblack.const import carbonblack_query_details


class CarbonBlackLogSourceSignature(LogSourceSignature):
    def is_suitable(self) -> bool:
        return True

    def __str__(self) -> str:
        return ""


class CarbonBlackMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> CarbonBlackLogSourceSignature:
        ...


carbonblack_query_mappings = CarbonBlackMappings(platform_dir="carbonblack", platform_details=carbonblack_query_details)
