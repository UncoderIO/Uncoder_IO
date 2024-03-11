import logging
from typing import Optional, Union

from app.translator.core.exceptions.core import UnsupportedPlatform
from app.translator.core.models.query_container import RawQueryContainer, TokenizedQueryContainer
from app.translator.core.parser import PlatformQueryParser
from app.translator.core.render import QueryRender
from app.translator.managers import ParserManager, RenderManager, parser_manager, render_manager
from app.translator.platforms.elasticsearch.const import ELASTIC_QUERY_TYPES
from app.translator.platforms.roota.parsers.roota import RootAParser
from app.translator.platforms.sigma.parsers.sigma import SigmaParser
from app.translator.tools.decorators import handle_translation_exceptions


class SiemConverter:
    renders: RenderManager = render_manager
    parsers: ParserManager = parser_manager

    def __init__(self):
        self.logger = logging.getLogger("siem_converter")

    def __get_parser(self, source: str) -> Union[PlatformQueryParser, RootAParser, SigmaParser]:
        parser = RootAParser() if source == "roota" else self.parsers.get(source)
        if not parser:
            raise UnsupportedPlatform(platform=source, is_parser=True)

        return parser

    def __get_render(self, target: str) -> QueryRender:
        if not (render := self.renders.get(target)):
            raise UnsupportedPlatform(platform=target)

        return render

    @staticmethod
    def __is_one_vendor_translation(source: str, target: str) -> bool:
        vendors_query_types = [ELASTIC_QUERY_TYPES]
        for vendor_query_types in vendors_query_types:
            if source in vendor_query_types and target in vendor_query_types:
                return True

        return False

    @handle_translation_exceptions
    def __parse_incoming_data(
        self, text: str, source: str, target: Optional[str] = None
    ) -> tuple[Optional[RawQueryContainer], Optional[TokenizedQueryContainer]]:
        parser = self.__get_parser(source)
        if isinstance(parser, SigmaParser):
            return None, parser.parse(text)

        raw_query_container = parser.parse_raw_query(text, language=source)
        tokenized_query_container = None
        if target and not self.__is_one_vendor_translation(raw_query_container.language, target):
            tokenized_query_container = parser.parse(raw_query_container)

        return raw_query_container, tokenized_query_container

    @handle_translation_exceptions
    def __render_translation(
        self, query_container: Union[RawQueryContainer, TokenizedQueryContainer], target: str
    ) -> str:
        render = self.__get_render(target)
        return render.generate(query_container)

    def __generate_one(self, text: str, source: str, target: str) -> (bool, str):
        status, parsed_data = self.__parse_incoming_data(text=text, source=source, target=target)
        if not status:
            return status, parsed_data

        raw_query_container, tokenized_query_container = parsed_data
        query_container = tokenized_query_container or raw_query_container
        return self.__render_translation(query_container=query_container, target=target)

    def __generate_all(self, text: str, source: str) -> list[dict]:
        status, parsed_data = self.__parse_incoming_data(text=text, source=source)
        if not status:
            return [{"status": status, "result": parsed_data, "siem_type": source}]

        raw_query_container, tokenized_query_container = parsed_data
        result = []
        for target in self.renders.all_platforms():
            if target == source:
                continue

            if raw_query_container and self.__is_one_vendor_translation(raw_query_container.language, target):
                status, data = self.__render_translation(query_container=raw_query_container, target=target)
            else:
                status, data = self.__render_translation(query_container=tokenized_query_container, target=target)
            result.append({"status": status, "result": data, "siem_type": target})

        return result

    def generate_translation(self, text: str, source: str, target: str) -> (bool, str):
        return self.__generate_one(text=text, source=source, target=target)

    def generate_all_translation(self, text: str, source: str) -> list[dict]:
        return self.__generate_all(text=text, source=source)

    def get_all_platforms(self) -> tuple:
        return self.get_renders(), self.get_parsers()

    def get_parsers(self) -> list:
        return self.parsers.get_platforms_details

    def get_renders(self) -> list:
        return self.renders.get_platforms_details
