import copy
import json

from app.translator.core.mapping import SourceMapping
from app.translator.core.models.parser_output import MetaInfoContainer
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.platforms.sumo_logic.renders.sumologic_cse import SumoLogicCSEQueryRender
from app.translator.platforms.sumo_logic.const import sumologic_cse_rule_details
from app.translator.platforms.sumo_logic.const import DEFAULT_SUMOLOGIC_CSE_RULE, SEVERITY_MAP


class SumoLogicCSERuleRender(SumoLogicCSEQueryRender):
    details: PlatformDetails = sumologic_cse_rule_details

    def finalize_query(self, prefix: str, query: str, functions: str, meta_info: MetaInfoContainer = None,
                       source_mapping: SourceMapping = None, not_supported_functions: list = None):
        query = super().finalize_query(prefix=prefix, query=query, functions=functions)
        rule = copy.deepcopy(DEFAULT_SUMOLOGIC_CSE_RULE)
        rule["name"] = meta_info.title or rule["name"]
        rule["description"] = meta_info.description or rule["description"]
        rule["score"] = SEVERITY_MAP.get(meta_info.severity)
        rule["expression"] = query

        return json.dumps(rule, indent=4, sort_keys=False)
