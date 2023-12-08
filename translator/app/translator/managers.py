from abc import ABC

from app.translator.platforms import __ALL_PARSERS as PARSERS
from app.translator.platforms import __ALL_RENDERS as RENDERS
from app.translator.platforms import __ALL_RENDERS_CTI as RENDERS_CTI
from app.translator.core.exceptions.core import UnsupportedRootAParser
from app.models.translation import ConvertorPlatform


class Manager(ABC):
    platforms_class = tuple()

    @property
    def platforms(self) -> dict:
        return {platform.details.siem_type: platform for platform in self.platforms_class}

    def get(self, siem):
        if platform := self.platforms.get(siem):
            return platform
        raise UnsupportedRootAParser(parser=siem)

    def all_platforms(self):
        return list(self.platforms)

    @property
    def get_platforms_details(self):
        platforms = [
            ConvertorPlatform(
                id=platform.details.siem_type,
                name=platform.details.name,
                code=platform.details.siem_type,
                group_name=platform.details.group_name,
                group_id=platform.details.group_id,
                platform_name=platform.details.platform_name,
                platform_id=platform.details.siem_type,
                alt_platform_name=platform.details.alt_platform_name,
                alt_platform=platform.details.alt_platform,
                first_choice=platform.details.first_choice,
            ) for platform in self.platforms_class
        ]
        return sorted(platforms, key=lambda platform: platform.group_name)


class RenderManager(Manager):
    platforms_class = RENDERS


class ParserManager(Manager):
    platforms_class = PARSERS


class RenderCTIManager(Manager):
    platforms_class = RENDERS_CTI


parser_manager = ParserManager()
render_manager = RenderManager()
render_cti_manager = RenderCTIManager()
