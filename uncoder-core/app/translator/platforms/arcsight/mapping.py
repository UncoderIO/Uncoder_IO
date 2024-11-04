from app.translator.core.mapping import BaseStrictLogSourcesPlatformMappings, LogSourceSignature
from app.translator.platforms.arcsight.const import arcsight_query_details


class ArcSightLogSourceSignature(LogSourceSignature):
    def is_suitable(self) -> bool:
        return True

    def __str__(self) -> str:
        return ""


class ArcSightMappings(BaseStrictLogSourcesPlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> ArcSightLogSourceSignature:  # noqa: ARG002
        return ArcSightLogSourceSignature()


arcsight_query_mappings = ArcSightMappings(platform_dir="arcsight", platform_details=arcsight_query_details)
