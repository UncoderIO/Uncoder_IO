from __future__ import annotations

from typing import TYPE_CHECKING

from app.translator.core.functions import PlatformFunctionsManager

if TYPE_CHECKING:
    from app.translator.platforms.base.spl.renders.spl import SplQueryRender


class SplFunctionsManager(PlatformFunctionsManager):
    def post_init_configure(self, platform_render: SplQueryRender) -> None:
        pass
