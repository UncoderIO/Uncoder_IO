from typing import Optional

from app.translator.core.mapping import DEFAULT_MAPPING_NAME, BasePlatformMappings, LogSourceSignature, SourceMapping


class AQLLogSourceSignature(LogSourceSignature):
    def __init__(
        self,
        device_types: Optional[list[int]],
        categories: Optional[list[int]],
        qids: Optional[list[int]],
        qid_event_categories: Optional[list[int]],
        default_source: dict,
    ):
        self.device_types = set(device_types or [])
        self.categories = set(categories or [])
        self.qids = set(qids or [])
        self.qid_event_categories = set(qid_event_categories or [])
        self._default_source = default_source or {}

    def is_suitable(
        self,
        devicetype: Optional[list[int]],
        category: Optional[list[int]],
        qid: Optional[list[int]],
        qideventcategory: Optional[list[int]],
    ) -> bool:
        device_type_match = set(devicetype).issubset(self.device_types) if devicetype else None
        category_match = set(category).issubset(self.categories) if category else None
        qid_match = set(qid).issubset(self.qids) if qid else None
        qid_event_category_match = (
            set(qideventcategory).issubset(self.qid_event_categories) if qideventcategory else None
        )
        all_conditions = [
            condition
            for condition in (device_type_match, category_match, qid_match, qid_event_category_match)
            if condition is not None
        ]
        return bool(all_conditions) and all(all_conditions)

    def __str__(self) -> str:
        return self._default_source.get("table", "events")

    @property
    def extra_condition(self) -> str:
        default_source = self._default_source
        return " AND ".join((f"{key}={value}" for key, value in default_source.items() if key != "table" and value))


class AQLMappings(BasePlatformMappings):
    skip_load_default_mappings: bool = False
    extend_default_mapping_with_all_fields: bool = True

    def prepare_log_source_signature(self, mapping: dict) -> AQLLogSourceSignature:
        log_source = mapping.get("log_source", {})
        default_log_source = mapping["default_log_source"]
        return AQLLogSourceSignature(
            device_types=log_source.get("devicetype"),
            categories=log_source.get("category"),
            qids=log_source.get("qid"),
            qid_event_categories=log_source.get("qideventcategory"),
            default_source=default_log_source,
        )

    def get_suitable_source_mappings(
        self,
        field_names: list[str],
        devicetype: Optional[list[int]] = None,
        category: Optional[list[int]] = None,
        qid: Optional[list[int]] = None,
        qideventcategory: Optional[list[int]] = None,
    ) -> list[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            log_source_signature: AQLLogSourceSignature = source_mapping.log_source_signature
            if log_source_signature.is_suitable(devicetype, category, qid, qideventcategory):  # noqa: SIM102
                if source_mapping.fields_mapping.is_suitable(field_names):
                    suitable_source_mappings.append(source_mapping)

        if not suitable_source_mappings:
            for source_mapping in self._source_mappings.values():
                if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                    continue
                if source_mapping.fields_mapping.is_suitable(field_names):
                    suitable_source_mappings.append(source_mapping)

        if not suitable_source_mappings:
            suitable_source_mappings = [self._source_mappings[DEFAULT_MAPPING_NAME]]

        return suitable_source_mappings
