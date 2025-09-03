"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2024 SOC Prime, Inc.

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

from app.translator.core.escape_manager import EscapeManager
from app.translator.core.custom_types.values import ValueType


class ExabeamEscapeManager(EscapeManager):
    escape_map = {
        ValueType.value: {
            '"': '\\"',
            "'": "\\'",
            "\\": "\\\\",
        },
        ValueType.regex_value: {
            '"': '\\"',
            "'": "\\'", 
            "\\": "\\\\",
        },
        ValueType.number_value: {},
        ValueType.bool_value: {},
    }