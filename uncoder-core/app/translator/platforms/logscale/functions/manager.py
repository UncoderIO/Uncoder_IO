from __future__ import annotations

from typing import TYPE_CHECKING

from app.translator.core.functions import PlatformFunctionsManager

if TYPE_CHECKING:
    from app.translator.platforms.logscale.renders.logscale import LogScaleQueryRender


class LogScaleFunctionsManager(PlatformFunctionsManager):
    def post_init_configure(self, platform_render: LogScaleQueryRender) -> None:
        pass
