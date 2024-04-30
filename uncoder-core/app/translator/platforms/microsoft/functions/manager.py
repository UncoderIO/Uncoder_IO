from __future__ import annotations

from typing import TYPE_CHECKING

from app.translator.core.functions import PlatformFunctionsManager

if TYPE_CHECKING:
    from app.translator.platforms.microsoft.renders.microsoft_sentinel import MicrosoftSentinelQueryRender


class MicrosoftFunctionsManager(PlatformFunctionsManager):
    def post_init_configure(self, platform_render: MicrosoftSentinelQueryRender) -> None:
        pass
