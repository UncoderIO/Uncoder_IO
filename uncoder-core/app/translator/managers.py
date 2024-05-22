from abc import ABC
from functools import cached_property
from typing import ClassVar, Union

from app.models.translation import TranslatorPlatform
from app.translator.core.exceptions.core import UnsupportedPlatform, UnsupportedRootAParser
from app.translator.core.parser import QueryParser
from app.translator.core.render import QueryRender
from app.translator.core.render_cti import RenderCTI


class PlatformManager(ABC):
    platforms: ClassVar[dict[str, Union[QueryParser, QueryRender, RenderCTI]]] = {}

    def all_platforms(self) -> list:
        return list(self.platforms.keys())

    @cached_property
    def get_platforms_details(self) -> list[TranslatorPlatform]:
        platforms = [
            TranslatorPlatform(
                id=platform.details.platform_id,
                name=platform.details.name,
                code=platform.details.platform_id,
                group_name=platform.details.group_name,
                group_id=platform.details.group_id,
                platform_name=platform.details.platform_name,
                platform_id=platform.details.platform_id,
                alt_platform_name=platform.details.alt_platform_name,
                alt_platform=platform.details.alt_platform,
                first_choice=platform.details.first_choice,
            )
            for platform in self.platforms.values()
        ]
        return sorted(platforms, key=lambda platform: platform.group_name)


class ParserManager(PlatformManager):
    supported_by_roota_platforms: ClassVar[dict[str, QueryParser]] = {}
    main_platforms: ClassVar[dict[str, QueryParser]] = {}

    def get(self, platform_id: str) -> QueryParser:
        if platform := self.platforms.get(platform_id):
            return platform
        raise UnsupportedPlatform(platform=platform_id, is_parser=True)

    def register(self, cls: type[QueryParser]) -> type[QueryParser]:
        self.platforms[cls.details.platform_id] = cls()
        return cls

    def get_supported_by_roota(self, platform_id: str) -> QueryParser:
        if platform := self.supported_by_roota_platforms.get(platform_id):
            return platform
        raise UnsupportedRootAParser(parser=platform_id)

    def register_supported_by_roota(self, cls: type[QueryParser]) -> type[QueryParser]:
        parser = cls()
        self.supported_by_roota_platforms[cls.details.platform_id] = parser
        self.platforms[cls.details.platform_id] = parser
        return cls

    def register_main(self, cls: type[QueryParser]) -> type[QueryParser]:
        parser = cls()
        self.main_platforms[cls.details.platform_id] = parser
        self.platforms[cls.details.platform_id] = parser
        return cls


class RenderManager(PlatformManager):
    platforms: ClassVar[dict[str, QueryRender]] = {}

    def get(self, platform_id: str) -> QueryRender:
        if platform := self.platforms.get(platform_id):
            return platform
        raise UnsupportedPlatform(platform=platform_id)

    def register(self, cls: type[QueryRender]) -> type[QueryRender]:
        self.platforms[cls.details.platform_id] = cls()
        return cls


class RenderCTIManager(PlatformManager):
    platforms: ClassVar[dict[str, RenderCTI]] = {}

    def get(self, platform_id: str) -> RenderCTI:
        if platform := self.platforms.get(platform_id):
            return platform
        raise UnsupportedPlatform(platform=platform_id)

    def register(self, cls: type[RenderCTI]) -> type[RenderCTI]:
        self.platforms[cls.details.platform_id] = cls()
        return cls


parser_manager = ParserManager()
render_manager = RenderManager()
render_cti_manager = RenderCTIManager()
