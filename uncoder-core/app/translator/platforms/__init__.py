import importlib.util
import os

from const import ROOT_PROJECT_PATH

platforms_path = ROOT_PROJECT_PATH + "/app/translator/platforms"
for platform in [f for f in os.listdir(platforms_path) if os.path.isdir(os.path.join(platforms_path, f))]:
    if "__" not in platform:
        init_path = f"{platforms_path}/{platform}/__init__.py"
        spec = importlib.util.spec_from_file_location("__init__", init_path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
