from typing import List, Optional

from app.converter.core.mapping import BasePlatformMappings, LogSourceSignature, SourceMapping, DEFAULT_MAPPING_NAME


class SigmaLogSourceSignature(LogSourceSignature):
    def __init__(self,
                 product: Optional[List[str]],
                 category: Optional[List[str]],
                 service: Optional[List[str]],
                 default_source: dict = None):
        self.products = set(product or [])
        self.categories = set(category or [])
        self.services = set(service or [])
        self._default_source = default_source or {}

    def is_suitable(self,
                    service: Optional[List[str]],
                    product: Optional[List[str]],
                    category: Optional[List[str]]) -> bool:
        product_match = set(product or []).issubset(self.products)
        category_match = set(category or []).issubset(self.categories)
        service_match = set(service or []).issubset(self.services)
        return product_match and category_match and service_match

    def __str__(self) -> str:
        raise NotImplementedError()

    @property
    def log_sources(self) -> dict:
        return self._default_source


class SigmaMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> SigmaLogSourceSignature:
        product = mapping.get("log_source", {}).get("product")
        service = mapping.get("log_source", {}).get("service")
        category = mapping.get("log_source", {}).get("category")
        default_log_source = mapping["default_log_source"]
        return SigmaLogSourceSignature(
            product=product,
            service=service,
            category=category,
            default_source=default_log_source
        )

    def get_suitable_source_mappings(self,
                                     field_names: List[str],
                                     product: List[str] = None,
                                     service: List[str] = None,
                                     category: List[str] = None) -> List[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            source_signature: SigmaLogSourceSignature = source_mapping.log_source_signature
            if source_signature.is_suitable(product=product, service=service, category=category):
                if source_mapping.fields_mapping.is_suitable(field_names):
                    suitable_source_mappings.append(source_mapping)

        return suitable_source_mappings or [self._source_mappings[DEFAULT_MAPPING_NAME]]


sigma_mappings = SigmaMappings(platform_dir="sigma")
