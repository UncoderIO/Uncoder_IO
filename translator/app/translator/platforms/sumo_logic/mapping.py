from typing import List, Optional

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature, SourceMapping, DEFAULT_MAPPING_NAME


class SumoLogicQueryLogSourceSignature(LogSourceSignature):
    def __init__(self,
                 event_channels: Optional[List[str]],
                 source_names: Optional[List[str]],
                 source_categories: Optional[List[str]],
                 default_source: dict = None):
        self.event_channels = set(event_channels or [])
        self.source_names = set(source_names or [])
        self.source_categories = set(source_categories or [])
        self._default_source = default_source or {}

    def is_suitable(self, *args, **kwargs) -> bool:
        return True

    def __str__(self) -> str:
        logsource_keys = []
        for key, value in self._default_source.items():
            if key == 'event_channel':
                logsource_keys.append(f'"{value}"')
            else:
                logsource_keys.append(f'{key}=*"{value}"*')
        return " AND ".join(logsource_keys)


class SumoLogicMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> SumoLogicQueryLogSourceSignature:
        log_source = mapping.get("log_source", {})
        default_log_source = mapping.get("default_log_source")
        return SumoLogicQueryLogSourceSignature(
            event_channels=log_source.get('event_channel'),
            source_names=log_source.get('_sourceName'),
            source_categories=log_source.get('_sourceCategory'),
            default_source=default_log_source
        )

    def get_suitable_source_mappings(self,
                                     event_channel: List[str] = None,
                                     source_name: List[str] = None,
                                     index: List[str] = None) -> List[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            source_signature: SumoLogicQueryLogSourceSignature = source_mapping.log_source_signature
            if source_signature.is_suitable(event_channel, source_name, index):
                if source_mapping.fields_mapping.is_suitable():
                    suitable_source_mappings.append(source_mapping)

        return suitable_source_mappings or [self._source_mappings[DEFAULT_MAPPING_NAME]]


sumologic_mappings = SumoLogicMappings(platform_dir="sumologic")