import os
from collections.abc import Generator

import yaml

from app.translator.const import APP_PATH

COMMON_FIELD_MAPPING_FILE_NAME = "common.yml"


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

    def load_siem_mappings(self, platform_dir: str) -> Generator[dict, None, None]:
        platform_path = os.path.join(self.base_mapping_filepath, platform_dir)
        for mapping_file in os.listdir(platform_path):
            if mapping_file != COMMON_FIELD_MAPPING_FILE_NAME:
                yield self.load_mapping(mapping_file_path=os.path.join(platform_path, mapping_file))

    def load_common_mapping(self, platform_dir: str) -> dict:
        platform_path = os.path.join(self.base_mapping_filepath, platform_dir)
        return self.load_mapping(mapping_file_path=os.path.join(platform_path, COMMON_FIELD_MAPPING_FILE_NAME))
