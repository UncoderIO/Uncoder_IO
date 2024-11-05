from app.translator.core.mapping import BasePlatformMappings, LogSourceSignature
from app.translator.platforms.falco.const import falco_rule_details


class FalcoRuleLogSourceSignature(LogSourceSignature):

    def is_suitable(self) -> bool:
        return True


class FalcoRuleMappings(BasePlatformMappings):

    def prepare_log_source_signature(self, mapping: dict) -> FalcoRuleLogSourceSignature:
        return FalcoRuleLogSourceSignature()


falco_rule_mappings = FalcoRuleMappings(platform_dir="falco", platform_details=falco_rule_details)
