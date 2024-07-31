from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature
from app.translator.platforms.chronicle.const import chronicle_query_details, chronicle_rule_details


class ChronicleLogSourceSignature(LogSourceSignature):
    def is_suitable(self) -> bool:
        return True

    def __str__(self) -> str:
        return ""


class ChronicleMappings(BasePlatformMappings):
    is_strict_mapping = True

    def prepare_log_source_signature(self, mapping: dict) -> ChronicleLogSourceSignature:
        ...


chronicle_query_mappings = ChronicleMappings(platform_dir="chronicle", platform_details=chronicle_query_details)
chronicle_rule_mappings = ChronicleMappings(platform_dir="chronicle", platform_details=chronicle_rule_details)
