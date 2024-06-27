from typing import Optional

from app.translator.core.mapping import DEFAULT_MAPPING_NAME, BasePlatformMappings, LogSourceSignature, SourceMapping


class SigmaLogSourceSignature(LogSourceSignature):
    def __init__(
        self,
        product: Optional[list[str]],
        category: Optional[list[str]],
        service: Optional[list[str]],
        default_source: dict = None,
    ):
        self.products = set(product or [])
        self.categories = set(category or [])
        self.services = set(service or [])
        self._default_source = default_source or {}

    def is_suitable(
        self, service: Optional[list[str]], product: Optional[list[str]], category: Optional[list[str]]
    ) -> bool:
        product_match = set(product_.lower() for product_ in product or []).issubset(self.products) if product else False
        category_match = set(category_.lower() for category_ in category or []).issubset(self.categories) if category else False
        service_match = set(service_.lower() for service_ in service or [] or []).issubset(self.services) if service else False
        if not product and not service:
            return category_match
        return product_match and service_match or product_match and category_match

    def __str__(self) -> str:
        raise NotImplementedError

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
            product=product, service=service, category=category, default_source=default_log_source
        )

    def get_suitable_source_mappings(
        self, field_names: list[str], product: list[str] = None, service: list[str] = None, category: list[str] = None
    ) -> list[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            source_signature: SigmaLogSourceSignature = source_mapping.log_source_signature
            if source_signature.is_suitable(product=product, service=service, category=category):
                suitable_source_mappings.append(source_mapping)

        return suitable_source_mappings or [self._source_mappings[DEFAULT_MAPPING_NAME]]


sigma_mappings = SigmaMappings(platform_dir="sigma")
