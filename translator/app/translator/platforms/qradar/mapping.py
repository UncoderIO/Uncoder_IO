from typing import List, Optional

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature, SourceMapping, DEFAULT_MAPPING_NAME


class QradarLogSourceSignature(LogSourceSignature):
    def __init__(self,
                 tables: Optional[List[str]],
                 device_types: Optional[List[int]],
                 categories: Optional[List[int]],
                 qids: Optional[List[int]],
                 qid_event_categories: Optional[List[int]],
                 default_source: dict):
        self.tables = set(tables or [])
        self.device_types = set(device_types or [])
        self.categories = set(categories or [])
        self.qids = set(qids or [])
        self.qid_event_categories = set(qid_event_categories or [])
        self._default_source = default_source or {}

    def is_suitable(self,
                    table: List[str],
                    devicetype: Optional[List[int]],
                    category: Optional[List[int]],
                    qid: Optional[List[int]],
                    qideventcategory: Optional[List[int]]) -> bool:
        table_match = set(table).issubset(self.tables)
        device_type_match = set(devicetype or []).issubset(self.device_types)
        category_match = set(category or []).issubset(self.categories)
        qid_match = set(qid or []).issubset(self.qids)
        qid_event_category_match = set(qideventcategory or []).issubset(self.qid_event_categories)

        return table_match and device_type_match and category_match and qid_match and qid_event_category_match

    def __str__(self) -> str:
        return self._default_source.get("table", "events")

    @property
    def extra_condition(self) -> str:
        default_source = self._default_source
        return " AND ".join((f"{key}={value}" for key, value in default_source.items() if key != "table" and value))


class QradarMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> QradarLogSourceSignature:
        log_source = mapping.get("log_source", {})
        default_log_source = mapping["default_log_source"]
        return QradarLogSourceSignature(
            tables=log_source.get("table"),
            device_types=log_source.get("devicetype"),
            categories=log_source.get("category"),
            qids=log_source.get("qid"),
            qid_event_categories=log_source.get("qideventcategory"),
            default_source=default_log_source
        )

    def get_suitable_source_mappings(self,
                                     field_names: List[str],
                                     table: List[str],
                                     devicetype: List[int] = None,
                                     category: List[int] = None,
                                     qid: List[int] = None,
                                     qideventcategory: List[int] = None) -> List[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            log_source_signature: QradarLogSourceSignature = source_mapping.log_source_signature
            if table and log_source_signature.is_suitable(table, devicetype, category, qid, qideventcategory):
                if source_mapping.fields_mapping.is_suitable(field_names):
                    suitable_source_mappings.append(source_mapping)
            else:
                if source_mapping.fields_mapping.is_suitable(field_names):
                    suitable_source_mappings.append(source_mapping)

        if not suitable_source_mappings:
            suitable_source_mappings = [self._source_mappings[DEFAULT_MAPPING_NAME]]

        return suitable_source_mappings


qradar_mappings = QradarMappings(platform_dir="qradar")
