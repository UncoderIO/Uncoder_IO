import logging

from app.converter.platforms.roota.parsers.roota import RootAParser
from app.converter.core.exceptions.core import UnsupportedPlatform
from app.converter.core.operator_types.output import SiemContainer
from app.converter.managers import RenderManager, ParserManager, render_manager, parser_manager
from app.converter.tools.decorators import handle_translation_exceptions


class SiemConverter:
    renders: RenderManager = render_manager
    parsers: ParserManager = parser_manager

    def __init__(self):
        self.logger = logging.getLogger("siem_converter")

    @handle_translation_exceptions
    def __parse_incoming_data(self, text: str, source: str) -> SiemContainer:
        parser = RootAParser() if source == "roota" else self.parsers.get(source)
        if not parser:
            raise UnsupportedPlatform(platform=source, is_parser=True)
        return parser.parse(text=text)

    @handle_translation_exceptions
    def __render_translation(self, parsed_data: SiemContainer, target: str) -> str:
        render = self.renders.get(target)
        if not render:
            raise UnsupportedPlatform(platform=target)
        return render.generate(
            query=parsed_data.query,
            meta_info=parsed_data.meta_info,
            functions=parsed_data.functions
        )

    def __generate_one_translation(self, text: str, source: str, target: str) -> (bool, str):
        status, parsed_data = self.__parse_incoming_data(text=text, source=source)
        if status:
            return self.__render_translation(parsed_data=parsed_data, target=target)
        return status, parsed_data

    def __generate_all(self, text: str, source: str) -> list[dict]:
        status, parsed_data = self.__parse_incoming_data(text=text, source=source)
        if status:
            result = []
            for target in self.renders.all_platforms():
                if target == source:
                    continue
                translation = {"siem_type": target}
                render_status, data = self.__render_translation(parsed_data=parsed_data, target=target)
                translation.update({"status": render_status, "result": data})
                result.append(translation)
            return result
        return [{"status": status, "result": parsed_data, "siem_type": source}]

    def generate_translation(self, text: str, source: str, target: str) -> (bool, str):
        return self.__generate_one_translation(text=text, source=source, target=target)

    def generate_all_translation(self, text: str, source: str) -> list[dict]:
        return self.__generate_all(text=text, source=source)

    def get_all_platforms(self) -> tuple:
        return self.get_renders(), self.get_parsers()

    def get_parsers(self) -> list:
        return self.parsers.get_platforms_details

    def get_renders(self) -> list:
        return self.renders.get_platforms_details
