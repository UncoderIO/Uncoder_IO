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
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.managers import render_manager
from app.translator.platforms.base.aql.renders.aql import AQLFieldValue, AQLQueryRender
from app.translator.platforms.qradar.const import qradar_query_details


class QradarFieldValue(AQLFieldValue):
    details: PlatformDetails = qradar_query_details


@render_manager.register
class QradarQueryRender(AQLQueryRender):
    details: PlatformDetails = qradar_query_details
