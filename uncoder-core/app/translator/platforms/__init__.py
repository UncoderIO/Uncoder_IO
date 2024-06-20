import os

from app.translator.tools.utils import execute_module
from const import PLATFORMS_PATH


def init_platforms() -> None:
    for platform in [f for f in os.listdir(PLATFORMS_PATH) if os.path.isdir(os.path.join(PLATFORMS_PATH, f))]:
        if not platform.startswith("__") and not platform.endswith("__"):
            # Platforms __init__.py execution
            execute_module(f"{PLATFORMS_PATH}/{platform}/__init__.py")


init_platforms()
