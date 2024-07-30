from typing import Optional

from app.translator.core.mapping import DEFAULT_MAPPING_NAME, BasePlatformMappings, LogSourceSignature, SourceMapping
from app.translator.platforms.sigma.const import sigma_rule_details


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
        self,
        service: Optional[list[str]] = None,
        product: Optional[list[str]] = None,
        category: Optional[list[str]] = None
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


sigma_rule_mappings = SigmaMappings(platform_dir="sigma", platform_details=sigma_rule_details)
