import logging
from typing import Dict, List

from app.converter.const import CTI_MIN_LIMIT_QUERY
from app.converter.core.models.iocs import IocsChunkValue
from app.converter.core.parser_cti import CTIParser, Iocs
from app.converter.core.render_cti import RenderCTI
from app.converter.managers import RenderCTIManager, render_cti_manager
from app.converter.tools.decorators import handle_translation_exceptions
from app.models.ioc_translation import CTIPlatform


class CTIConverter:
    renders: RenderCTIManager = render_cti_manager

    def __init__(self):
        self.logger = logging.getLogger("cti_converter")
        self.parser = CTIParser()

    def _get_render_mapping(self, platform: CTIPlatform, include_source_ip: bool = False) -> Dict[str, str]:
        return self.renders.get(platform.name).default_mapping

    @handle_translation_exceptions
    def __parse_iocs_from_string(self, text: str, include_ioc_types: list = None, include_hash_types: list = None,
                                 exceptions: list = None, ioc_parsing_rules: list = None) -> Iocs:
        return self.parser.get_iocs_from_string(string=text,
                                                include_ioc_types=include_ioc_types,
                                                include_hash_types=include_hash_types,
                                                exceptions=exceptions,
                                                ioc_parsing_rules=ioc_parsing_rules,
                                                limit=CTI_MIN_LIMIT_QUERY)

    @handle_translation_exceptions
    def __render_translation(self, parsed_data: dict, platform_data: CTIPlatform, iocs_per_query: int,
                             include_source_ip: bool = False) -> List[str]:
        mapping = self._get_render_mapping(platform=platform_data, include_source_ip=include_source_ip)
        platform = self.renders.get(platform_data.name)
        platform_generation = self.generate(data=parsed_data, platform=platform, iocs_per_query=iocs_per_query,
                                            mapping=mapping)
        return platform_generation

    def convert(self, text: str,
                platform_data: CTIPlatform,
                iocs_per_query: int = 25,
                include_ioc_types: list = None,
                include_hash_types: list = None,
                exceptions: list = None,
                ioc_parsing_rules: list = None,
                include_source_ip: bool = False) -> (bool, List[str]):
        status, parsed_data = self.__parse_iocs_from_string(text=text,
                                                            include_ioc_types=include_ioc_types,
                                                            include_hash_types=include_hash_types,
                                                            exceptions=exceptions,
                                                            ioc_parsing_rules=ioc_parsing_rules)
        if status:
            return self.__render_translation(parsed_data=parsed_data,
                                             include_source_ip=include_source_ip,
                                             platform_data=platform_data,
                                             iocs_per_query=iocs_per_query
                                             )
        return status, parsed_data

    @staticmethod
    def _get_iocs_chunk(chunks_size: int, data: Dict[str, List[str]],
                        mapping: Dict[str, str]) -> List[List[IocsChunkValue]]:
        result = []
        for generic_field, iocs_list in data.items():
            for ioc in iocs_list:
                if mapping.get(generic_field):
                    result.append(IocsChunkValue(generic_field=generic_field,
                                                 platform_field=mapping[generic_field],
                                                 value=ioc))
        return [result[i:i + chunks_size] for i in range(0, len(result), chunks_size)]

    def generate(self, platform: RenderCTI, iocs_per_query, data: Dict[str, List[str]],
                 mapping: Dict[str, str]) -> List[str]:
        chunked_iocs = self._get_iocs_chunk(chunks_size=iocs_per_query, data=data, mapping=mapping)
        return platform.render(chunked_iocs)

    @classmethod
    def get_renders(cls) -> list:
        return cls.renders.get_platforms_details
