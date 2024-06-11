from typing import Optional, Union

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature



class SumoLogicQueryLogSourceSignature(LogSourceSignature):
    def __init__(self,
        source_names: Optional[list[str]],
        source_categories: Optional[list[str]],
        default_source: Union[dict, None] = None
    ):
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
        log_source: dict = mapping.get("log_source", {})
        default_log_source: dict | None = mapping.get("default_log_source")
        return SumoLogicQueryLogSourceSignature(
            source_names=log_source.get('_sourceName'),
            source_categories=log_source.get('_sourceCategory'),
            default_source=default_log_source
        )


class SumoLogicCSELogSourceSignature(LogSourceSignature):
    def __init__(self,
        source_names: Optional[list[str]],
        source_categories: Optional[list[str]],
        default_source: Union[dict, None] = None
    ):
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


class SumoLogicCSEMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> SumoLogicCSELogSourceSignature:
        log_source: dict = mapping.get("log_source", {})
        default_log_source: dict | None = mapping.get("default_log_source")
        return SumoLogicCSELogSourceSignature(
            source_names=log_source.get('_sourceName'),
            source_categories=log_source.get('_sourceCategory'),
            default_source=default_log_source
        )


sumologic_mappings = SumoLogicMappings(platform_dir="sumologic")