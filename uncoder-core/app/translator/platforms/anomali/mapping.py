from app.translator.core.mapping import BaseCommonPlatformMappings, LogSourceSignature
from app.translator.platforms.anomali.const import anomali_query_details


class AnomaliLogSourceSignature(LogSourceSignature):
    def is_suitable(self) -> bool:
        return True

    def __str__(self) -> str:
        return ""


class AnomaliMappings(BaseCommonPlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> AnomaliLogSourceSignature:  # noqa: ARG002
        return AnomaliLogSourceSignature()


anomali_query_mappings = AnomaliMappings(platform_dir="anomali", platform_details=anomali_query_details)
