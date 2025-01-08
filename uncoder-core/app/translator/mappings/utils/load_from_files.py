import os
from collections.abc import Generator

import yaml

from app.translator.const import APP_PATH

COMMON_FIELD_MAPPING_FILE_NAME = "common.yml"
DEFAULT_FIELD_MAPPING_FILE_NAME = "default.yml"
ALTERNATIVE_MAPPINGS_FOLDER_NAME = "alternative"


class LoaderFileMappings:
    base_mapping_filepath = os.path.join(APP_PATH, "mappings/platforms")

    @staticmethod
    def load_mapping(mapping_file_path: str) -> dict:
        with open(mapping_file_path) as yaml_obj:
            try:
                return yaml.safe_load(yaml_obj)
            except yaml.YAMLError as err:
                print(err)
                return {}

    def get_platform_alternative_mappings_dirs(self, platform_dir: str) -> dict[str:str]:
        platform_path = os.path.join(self.base_mapping_filepath, platform_dir, ALTERNATIVE_MAPPINGS_FOLDER_NAME)
        for _, dirs, _ in os.walk(platform_path):
            result = {}
            for folder in dirs:
                result[folder] = os.path.join(platform_dir, ALTERNATIVE_MAPPINGS_FOLDER_NAME, folder)
            return result
        return {}

    def load_platform_mappings(self, platform_dir: str) -> Generator[dict, None, None]:
        platform_path = os.path.join(self.base_mapping_filepath, platform_dir)
        for mapping_file in os.listdir(platform_path):
            if mapping_file.endswith(".yml") and mapping_file not in (
                COMMON_FIELD_MAPPING_FILE_NAME,
                DEFAULT_FIELD_MAPPING_FILE_NAME,
            ):
                yield self.load_mapping(mapping_file_path=os.path.join(platform_path, mapping_file))
        yield self.load_mapping(mapping_file_path=os.path.join(platform_path, DEFAULT_FIELD_MAPPING_FILE_NAME))

    def load_common_mapping(self, platform_dir: str) -> dict:
        platform_path = os.path.join(self.base_mapping_filepath, platform_dir)
        return self.load_mapping(mapping_file_path=os.path.join(platform_path, COMMON_FIELD_MAPPING_FILE_NAME))
