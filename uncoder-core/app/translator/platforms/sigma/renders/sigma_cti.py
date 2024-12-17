import uuid
import yaml

from app.translator.core.custom_types.meta_info import SeverityType
from app.translator.core.models.iocs import IocsChunkValue
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render_cti import RenderCTI
from app.translator.managers import render_cti_manager
from app.translator.platforms.sigma.const import sigma_rule_details, DEFAULT_SIGMA_CTI_MAPPING


@render_cti_manager.register
class SigmaRenderCTI(RenderCTI):
    details: PlatformDetails = sigma_rule_details
    default_mapping = DEFAULT_SIGMA_CTI_MAPPING

    def render(self, data: list[list[IocsChunkValue]]) -> list[str]:
        final_result = []
        for iocs_chunk in data:
            data_values = self.collect_sigma_data_values(iocs_chunk)
            rule = {
                    "title": "Sigma automatically generated based on IOCs",
                    "id":  uuid.uuid4().__str__(),
                    "description": "Detects suspicious activity based on IOCs.",
                    "status": "experimental",
                    "author": "SOC Prime",
                    "logsource": {"product": "windows"},
                    "fields": list(data_values.keys()),
                    "detection": {"selection": data_values, "condition": "selection"},
                    "level": SeverityType.low,
                    "falsepositives": "",
                }
            final_result.append(yaml.dump(rule, default_flow_style=False, sort_keys=False))
        return final_result

    def collect_sigma_data_values(self, chunk: list[IocsChunkValue]) -> dict:
        raw_data_values = {}
        for value in chunk:
            if value.platform_field in raw_data_values.keys():
                raw_data_values[value.platform_field].append(value.value)
            else:
                raw_data_values[value.platform_field] = [value.value]
        return raw_data_values
