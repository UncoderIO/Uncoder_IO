import importlib.util
import os

from const import PLATFORMS_PATH


def init_platforms():
    for platform in [f for f in os.listdir(PLATFORMS_PATH) if os.path.isdir(os.path.join(PLATFORMS_PATH, f))]:
        if not platform.startswith("__") and not platform.endswith("__"):
            # Platforms __init__.py execution
            init_path = f"{PLATFORMS_PATH}/{platform}/__init__.py"
            spec = importlib.util.spec_from_file_location("__init__", init_path)
            init_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(init_module)


init_platforms()
