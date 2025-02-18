import logging
from typing import Optional

from app.models.ioc_translation import CTIPlatform
from app.translator.const import CTI_IOCS_PER_QUERY_LIMIT, CTI_MIN_LIMIT_QUERY
from app.translator.core.models.iocs import IocsChunkValue
from app.translator.core.parser_cti import CTIParser
from app.translator.managers import RenderCTIManager, render_cti_manager
from app.translator.tools.decorators import handle_translation_exceptions


class CTITranslator:
    render_manager: RenderCTIManager = render_cti_manager

    def __init__(self):
        self.logger = logging.getLogger("cti_translator")
        self.parser = CTIParser()

    @handle_translation_exceptions
    def __parse_iocs_from_string(
        self,
        text: str,
        include_ioc_types: Optional[list] = None,
        include_hash_types: Optional[list] = None,
        exceptions: Optional[list] = None,
        ioc_parsing_rules: Optional[list] = None,
        include_source_ip: bool = False,
    ) -> dict:
        return self.parser.get_iocs_from_string(
            string=text,
            include_ioc_types=include_ioc_types,
            include_hash_types=include_hash_types,
            exceptions=exceptions,
            ioc_parsing_rules=ioc_parsing_rules,
            limit=CTI_MIN_LIMIT_QUERY,
            include_source_ip=include_source_ip,
        )

    @handle_translation_exceptions
    def __render_translation(self, parsed_data: dict, platform_data: CTIPlatform, iocs_per_query: int) -> list[str]:
        render_cti = self.render_manager.get(platform_data.id)

        chunked_iocs = self.__get_iocs_chunk(
            chunks_size=iocs_per_query, data=parsed_data, mapping=render_cti.default_mapping
        )
        return render_cti.render(chunked_iocs)

    def translate(
        self,
        text: str,
        platform_data: CTIPlatform,
        iocs_per_query: int = CTI_IOCS_PER_QUERY_LIMIT,
        include_ioc_types: Optional[list] = None,
        include_hash_types: Optional[list] = None,
        exceptions: Optional[list] = None,
        ioc_parsing_rules: Optional[list] = None,
        include_source_ip: bool = False,
    ) -> (bool, list[str]):
        status, parsed_data = self.__parse_iocs_from_string(
            text=text,
            include_ioc_types=include_ioc_types,
            include_hash_types=include_hash_types,
            exceptions=exceptions,
            ioc_parsing_rules=ioc_parsing_rules,
            include_source_ip=include_source_ip,
        )
        if status:
            return self.__render_translation(
                parsed_data=parsed_data, platform_data=platform_data, iocs_per_query=iocs_per_query
            )
        return status, parsed_data

    @staticmethod
    def __get_iocs_chunk(
        chunks_size: int, data: dict[str, list[str]], mapping: dict[str, str]
    ) -> list[list[IocsChunkValue]]:
        result = []
        for generic_field, iocs_list in data.items():
            for ioc in iocs_list:
                if mapping.get(generic_field):
                    result.append(
                        IocsChunkValue(generic_field=generic_field, platform_field=mapping[generic_field], value=ioc)
                    )
        return [result[i : i + chunks_size] for i in range(0, len(result), chunks_size)]

    @classmethod
    def get_renders(cls) -> list:
        return cls.render_manager.get_platforms_details


cti_translator = CTITranslator()
