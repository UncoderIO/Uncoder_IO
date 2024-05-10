from abc import ABC
from functools import cached_property

from app.models.translation import TranslatorPlatform
from app.translator.core.exceptions.core import UnsupportedRootAParser


class Manager(ABC):
    platforms = {}

    def register(self, cls):
        self.platforms[cls.details.platform_id] = cls()
        return cls

    def get(self, platform_id: str):  # noqa: ANN201
        if platform := self.platforms.get(platform_id):
            return platform
        raise UnsupportedRootAParser(parser=platform_id)

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


class ParserManager(Manager):
    platforms = {}
    supported_by_roota_platforms = {}
    main_platforms = {}

    def get_supported_by_roota(self, platform_id: str):  # noqa: ANN201
        if platform := self.supported_by_roota_platforms.get(platform_id):
            return platform
        raise UnsupportedRootAParser(parser=platform_id)

    def register_supported_by_roota(self, cls):
        parser = cls()
        self.supported_by_roota_platforms[cls.details.platform_id] = parser
        self.platforms[cls.details.platform_id] = parser
        return cls

    def register_main(self, cls):
        parser = cls()
        self.main_platforms[cls.details.platform_id] = parser
        self.platforms[cls.details.platform_id] = parser
        return cls

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


class RenderManager(Manager):
    platforms = {}


class RenderCTIManager(Manager):
    platforms = {}


parser_manager = ParserManager()
render_manager = RenderManager()
render_cti_manager = RenderCTIManager()
