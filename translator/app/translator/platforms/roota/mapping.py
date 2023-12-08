from typing import List

from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature, SourceMapping, DEFAULT_MAPPING_NAME


class RootaLogSourceSignature(LogSourceSignature):
    def __init__(self, product: List[str] = None, category: List[str] = None, service: List[str] = None, default_source: dict = None):
        self.products = set(product or [])
        self.categories = set(category or [])
        self.services = set(service or [])
        self._default_source = default_source or {}

    def is_suitable(self, service: str, product: str, category: str,) -> bool:
        product_match = product in self.products
        category_match = category in self.categories
        service_match = service in self.services
        return product_match and category_match and service_match

    @property
    def default_source(self) -> str:
        return self._default_source


class RootaMappings(BasePlatformMappings):
    def prepare_source(self, mapping: dict) -> SourceMapping:
        product = mapping.get("log_source", {}).get("product")
        service = mapping.get("log_source", {}).get("service")
        category = mapping.get("log_source", {}).get("category")
        default_log_source = mapping["default_log_source"]
        return SourceMapping(
            source_id=mapping["source"],
            source_signature=RootaLogSourceSignature(product=product,
                                                     service=service,
                                                     category=category,
                                                     default_source=default_log_source)
        )

    def get_log_source_id(self, product: str, service: str, category: str) -> str:
        for source in self.sources_mapping.values():
            source_signature: RootaLogSourceSignature = source.source_signature
            if source_signature.is_suitable(product=product, service=service, category=category):
                return source.source_id

        return DEFAULT_MAPPING_NAME


roota_mappings = RootaMappings(platform_dir="roota")
