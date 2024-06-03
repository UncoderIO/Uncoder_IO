from __future__ import annotations

from typing import TYPE_CHECKING

from app.translator.core.functions import PlatformFunctionsManager

if TYPE_CHECKING:
    from app.translator.platforms.palo_alto.renders.cortex_xsiam import CortexXQLQueryRender


class CortexXQLFunctionsManager(PlatformFunctionsManager):

    def post_init_configure(self, platform_render: CortexXQLQueryRender) -> None:
        ...
