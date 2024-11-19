from app.translator.core.mapping import BaseStrictLogSourcesPlatformMappings, LogSourceSignature
from app.translator.platforms.falco.const import falco_rule_details


class FalcoRuleLogSourceSignature(LogSourceSignature):
    def __str__(self) -> str:
        return ""

    def is_suitable(self) -> bool:
        return True


class FalcoRuleMappings(BaseStrictLogSourcesPlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> FalcoRuleLogSourceSignature:  # noqa: ARG002
        return FalcoRuleLogSourceSignature()


falco_rule_mappings = FalcoRuleMappings(platform_dir="falco", platform_details=falco_rule_details)
