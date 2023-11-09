"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2023 SOC Prime, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------
"""

from typing import List

from app.converter.core.models.iocs import IocsChunkValue


class RenderCTI:

    # EXAMPLE OF A BACKEND ATTRIBUTES
    data_map: str = "{key} =~ '{value}'"
    or_operator: str = " or "
    group_or_operator: str = " or "
    or_group: str = "({or_group})"
    result_join: str = ""
    final_result_for_many: str = "union * | where ({result})\n"
    final_result_for_one: str = "union * | where {result}\n"
    default_mapping = None

    def get_default_mapping(self, include_source_ip=False):
        return self.prepare_mapping(self.default_mapping, include_source_ip)

    def create_field_value(self, field: str, value: str, generic_field: str):
        return self.data_map.format(key=field, value=value)

    def render(self, data: List[List[IocsChunkValue]]) -> list[str]:
        final_result = []
        for iocs_chunk in data:
            data_values = self.collect_data_values(iocs_chunk)
            if len(data_values) > 1:
                final_result.append(self.final_result_for_many.format(result=self.group_or_operator.join(data_values)))
            else:
                final_result.append(self.final_result_for_one.format(result=data_values[0]))
        return final_result

    def collect_data_values(self, chunk):
        data_values = []
        key_chunk = []
        processing_key = chunk[0].generic_field
        for value in chunk:
            if processing_key != value.generic_field:
                data_values.append(self.or_group.format(or_group=self.or_operator.join(key_chunk),
                                                        processing_key=processing_key))
                key_chunk = []
                processing_key = value.generic_field
            key_chunk.append(self.create_field_value(field=value.generic_field,
                                                     value=value.value,
                                                     generic_field=value.generic_field))
        if key_chunk:
            data_values.append(
                self.or_group.format(or_group=self.or_operator.join(key_chunk), processing_key=processing_key))
        return data_values

    def prepare_mapping(self, mapping: dict, include_source_ip: bool = False) -> dict:
        m = {
            "DestinationIP": "ip",
            "Domain": "domain",
            "URL": "url",
            "HashMd5": "hash",
            "HashSha1": "hash",
            "HashSha256": "hash",
            "HashSha512": "hash",
        }
        if include_source_ip:
            m["SourceIP"] = "ip"
        res = {}
        for key, new_field_name in mapping.items():
            if key in m:
                res[new_field_name] = m[key]
        return res
