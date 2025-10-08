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

import json
import uuid
import os
from typing import Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.core.custom_types.values import ValueType
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.render import BaseFieldValueRender, PlatformQueryRender
from app.translator.core.str_value_manager import StrValue
from app.translator.managers import render_manager
from app.translator.platforms.exabeam.const import (
    EXABEAM_ANALYTICS_RULE_TEMPLATE,
    EXABEAM_CORRELATION_RULE_TEMPLATE,
    exabeam_analytics_rule_details,
    exabeam_correlation_rule_details,
    exabeam_eql_query_details,
)
from app.translator.platforms.base.lucene.str_value_manager import lucene_str_value_manager
from app.translator.platforms.exabeam.escape_manager import ExabeamEscapeManager
from app.translator.platforms.exabeam.mapping import ExabeamMappings


class ExabeamEQLFieldValueRender(BaseFieldValueRender):
    details: PlatformDetails = exabeam_eql_query_details
    escape_manager = ExabeamEscapeManager()
    str_value_manager = lucene_str_value_manager
    
    def _escape_regex_value(self, value: str) -> str:
        """Escape regex special characters for use in RGX() expressions"""
        if isinstance(value, str):
            # Remove quotes if present
            value = value.strip('"\'')
            # Only escape the essential regex metacharacters that need escaping
            # Avoid double-escaping by handling backslashes first
            value = value.replace('\\', '\\\\')  # Handle backslashes first
            value = value.replace('.', '\\.')    # Escape dots
            # Don't escape other regex chars as they might be intentional
        return value
    
    @staticmethod
    def _wrap_str_value(value: str) -> str:
        """Wrap string values in quotes for EQL"""
        return f'"{value}"'

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f"{field} = {self._pre_process_value(field, val, wrap_str=True)}" for val in value)
            return f"({values})"
        return f"{field} = {self._pre_process_value(field, value, wrap_str=True)}"

    def less_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field} < {self._pre_process_value(field, value, wrap_str=True)}"

    def less_or_equal_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field} <= {self._pre_process_value(field, value, wrap_str=True)}"

    def greater_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field} > {self._pre_process_value(field, value, wrap_str=True)}"

    def greater_or_equal_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        return f"{field} >= {self._pre_process_value(field, value, wrap_str=True)}"

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            # Use De Morgan's law: NOT (A OR B) = NOT A AND NOT B
            values = self.and_token.join(f"{field} != {self._pre_process_value(field, val, wrap_str=True)}" for val in value)
            return f"({values})"
        return f"{field} != {self._pre_process_value(field, value, wrap_str=True)}"

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f"{field} = RGX(\".*{self._escape_regex_value(val)}.*\")" for val in self._pre_process_values_list(field, value))
            return f"({values})"
        escaped_value = self._escape_regex_value(self._pre_process_value(field, value))
        return f"{field} = RGX(\".*{escaped_value}.*\")"

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f"{field} = RGX(\"{self._escape_regex_value(val)}$\")" for val in self._pre_process_values_list(field, value))
            return f"({values})"
        escaped_value = self._escape_regex_value(self._pre_process_value(field, value))
        return f"{field} = RGX(\"{escaped_value}$\")"

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f"{field} = RGX(\"^{self._escape_regex_value(val)}\")" for val in self._pre_process_values_list(field, value))
            return f"({values})"
        escaped_value = self._escape_regex_value(self._pre_process_value(field, value))
        return f"{field} = RGX(\"^{escaped_value}\")"

    def regex_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        processed_value = self._pre_process_value(field, value, ValueType.regex_value)
        # Remove quotes if present for regex pattern
        if isinstance(processed_value, str):
            processed_value = processed_value.strip('"\'')
        return f"{field} = RGX(\"{processed_value}\")"

    def not_contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f"{field} != RGX(\".*{self._escape_regex_value(val)}.*\")" for val in self._pre_process_values_list(field, value))
            return f"({values})"
        escaped_value = self._escape_regex_value(self._pre_process_value(field, value))
        return f"{field} != RGX(\".*{escaped_value}.*\")"

    def not_endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f"{field} != RGX(\"{self._escape_regex_value(val)}$\")" for val in self._pre_process_values_list(field, value))
            return f"({values})"
        escaped_value = self._escape_regex_value(self._pre_process_value(field, value))
        return f"{field} != RGX(\"{escaped_value}$\")"

    def not_startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            values = self.or_token.join(f"{field} != RGX(\"^{self._escape_regex_value(val)}\")" for val in self._pre_process_values_list(field, value))
            return f"({values})"
        escaped_value = self._escape_regex_value(self._pre_process_value(field, value))
        return f"{field} != RGX(\"^{escaped_value}\")"

    def not_regex_modifier(self, field: str, value: Union[int, str, StrValue]) -> str:
        processed_value = self._pre_process_value(field, value, ValueType.regex_value)
        if isinstance(processed_value, str):
            processed_value = processed_value.strip('"\'')
        return f"{field} != RGX(\"{processed_value}\")"

    def is_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        return f"{field} = null"

    def is_not_none(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        return f"{field} != null"

    def keywords_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        return self.contains_modifier(field, value)


@render_manager.register
class ExabeamEQLQueryRender(PlatformQueryRender):
    details: PlatformDetails = exabeam_eql_query_details
    mappings: ExabeamMappings = ExabeamMappings(
        platform_dir="exabeam", platform_details=exabeam_eql_query_details
    )

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_render = ExabeamEQLFieldValueRender(or_token=or_token)
    query_pattern = "{prefix} SELECT {fields} {table} WHERE {query}"
    comment_symbol = "//"

    def generate_prefix(self, log_source_signature: dict, functions_prefix: str = "") -> str:
        return ""

    def generate_fields(self, log_source_signature: dict) -> str:
        return "*"

    def generate_table(self, log_source_signature: dict) -> str:
        return ""

    def wrap_with_comment(self, content: str) -> str:
        return f"// {content}"

    def finalize_query(
        self,
        prefix: str,
        query: str,
        functions: str,
        meta_info: dict = None,
        source_mapping: dict = None,
        not_supported_functions: list = None,
        unmapped_fields: list = None,
        *args,
        **kwargs,
    ) -> str:
        fields = self.generate_fields({})
        table = self.generate_table({})
        
        result_query = self.query_pattern.format(
            prefix=prefix,
            fields=fields,
            table=table,
            query=query
        ).strip()
        
        if not_supported_functions:
            result_query = f"{result_query}\n{self.wrap_with_comment('Unsupported functions: ' + ', '.join(not_supported_functions))}"
        
        if unmapped_fields:
            result_query = f"{result_query}\n{self.wrap_with_comment('Unmapped fields: ' + ', '.join(unmapped_fields))}"
            
        return result_query


@render_manager.register  
class ExabeamAnalyticsRuleRender(PlatformQueryRender):
    details: PlatformDetails = exabeam_analytics_rule_details
    mappings: ExabeamMappings = ExabeamMappings(
        platform_dir="exabeam", platform_details=exabeam_analytics_rule_details
    )

    or_token = "||"
    and_token = "&&" 
    not_token = "!"

    field_value_render = ExabeamEQLFieldValueRender(or_token=or_token)
    comment_symbol = "//"

    def generate_prefix(self, log_source_signature: dict, functions_prefix: str = "") -> str:
        return ""

    def wrap_with_comment(self, content: str) -> str:
        return f"// {content}"

    def finalize_query(
        self,
        prefix: str,
        query: str,
        functions: str,
        meta_info: dict = None,
        source_mapping: dict = None,
        not_supported_functions: list = None,
        unmapped_fields: list = None,
        *args,
        **kwargs,
    ) -> str:
        import copy
        rule = copy.deepcopy(EXABEAM_ANALYTICS_RULE_TEMPLATE)
        
        # Get the rule definition object
        rule_def = rule["ruleDefinitions"][0]
        
        # Generate unique template ID
        rule_def["templateId"] = f"Fact-UC-{str(uuid.uuid4())[:8]}"
        
        # Use rule title from meta_info or generate default
        rule_def["name"] = getattr(meta_info, 'title', None) or "Uncoder Generated Analytics Rule"
        rule_def["description"] = getattr(meta_info, 'description', None) or f"Analytics rule generated from rule translation"
        rule_def["detectionReason"] = rule_def["name"]
        
        # Set EQL condition
        rule_def["actOnCondition"] = query
        
        # Map activity types from meta_info logsource
        activity_type = "process-create"  # Default
        if meta_info and hasattr(meta_info, 'logsource') and meta_info.logsource:
            if hasattr(meta_info.logsource, 'category') and meta_info.logsource.category:
                activity_type = self._map_category_to_activity(meta_info.logsource.category)
        
        rule_def["applicableEvents"] = [{"activity_type": activity_type}]
        
        # Map severity
        if meta_info and hasattr(meta_info, 'severity'):
            severity_map = {
                "low": "Low",
                "medium": "Medium", 
                "high": "High",
                "critical": "Critical"
            }
            rule_def["severity"] = severity_map.get(str(meta_info.severity).lower(), "Medium")
        
        # Extract MITRE mapping if available
        if meta_info and hasattr(meta_info, 'tags') and meta_info.tags:
            mitre_tags = [tag for tag in meta_info.tags if tag.startswith("attack.")]
            if mitre_tags:
                mitre_mappings = []
                for tag in mitre_tags:
                    technique_key = tag.replace("attack.", "").upper()
                    if technique_key.startswith("T"):
                        technique_info = self._get_mitre_technique_info(technique_key)
                        if technique_info:
                            mitre_mappings.append(technique_info)
                
                if mitre_mappings:
                    rule_def["mitre"] = mitre_mappings[:3]  # Limit to 3 MITRE techniques
        
        # Set use cases based on rule content
        use_cases = self._infer_use_cases(query, meta_info)
        rule_def["useCases"] = [use_case.replace("_", " ") for use_case in use_cases]
        
        # Use predefined Exabeam family ID from valid families list
        rule_def["familyId"] = self._get_valid_family_id(rule_def["applicableEvents"])
        
        # Set corresponding valid rule group ID
        rule_def["ruleGroupId"] = self._get_valid_rule_group_id(rule_def["familyId"])
        
        if not_supported_functions:
            rule_def["description"] += f" Note: Unsupported functions: {', '.join(not_supported_functions)}"
        
        if unmapped_fields:
            rule_def["description"] += f" Note: Unmapped fields: {', '.join(unmapped_fields)}"
        
        return json.dumps(rule, indent=2)

    def _get_mitre_technique_info(self, technique_key: str) -> dict:
        """Get MITRE technique information from Uncoder's dictionaries"""
        try:
            techniques_path = "/siem_converter/app/dictionaries/techniques.json"
            with open(techniques_path, 'r') as f:
                techniques = json.load(f)
            
            tactics_path = "/siem_converter/app/dictionaries/tactics.json"
            with open(tactics_path, 'r') as f:
                tactics = json.load(f)
            
            # Find the technique
            for technique_data in techniques:
                if technique_data.get("technique") == technique_key:
                    # Get the first tactic for this technique
                    technique_tactics = technique_data.get("tactics", [])
                    if technique_tactics:
                        tactic_key = technique_tactics[0]
                        # Find tactic name
                        tactic_name = "Execution"  # Default
                        for tactic_data in tactics:
                            if tactic_data.get("tactic") == tactic_key:
                                tactic_name = tactic_data.get("name", "Execution")
                                break
                        
                        return {
                            "techniqueKey": technique_key,
                            "technique": technique_data.get("technique", technique_key),
                            "tactic": tactic_name,
                            "tacticKey": tactic_key or "TA0002"  # Default to Execution
                        }
        except Exception as e:
            print(f"Error loading MITRE data: {e}")
        
        return None

    def _map_category_to_activity(self, category: str) -> str:
        category_mapping = {
            "process_creation": "process-create",
            "network_connection": "network-connection", 
            "file_event": "file-event",
            "registry_event": "registry-event",
            "authentication": "authentication",
            "firewall": "firewall-activity",
        }
        return category_mapping.get(category, "process-create")

    def _infer_use_cases(self, query: str, meta_info) -> list:
        query_lower = query.lower()
        use_cases = []
        
        if any(term in query_lower for term in ["password", "credential", "auth", "login"]):
            use_cases.append("Compromised Credentials")
        if any(term in query_lower for term in ["privilege", "admin", "elevated", "system"]):
            use_cases.append("Privilege Escalation")  
        if any(term in query_lower for term in ["malware", "virus", "trojan", "backdoor"]):
            use_cases.append("Malware")
        if any(term in query_lower for term in ["exfil", "data", "transfer", "download"]):
            use_cases.append("Data Exfiltration")
        
        return use_cases or ["Malware"]

    def _get_valid_family_id(self, applicable_events: list) -> str:
        """Map activity types to valid Exabeam predefined families"""
        if applicable_events and applicable_events[0].get("activity_type"):
            activity = applicable_events[0]["activity_type"]
            
            # Map to valid Exabeam families from documentation
            family_mapping = {
                "process-create": "process-creation-activity",
                "network-connection": "network-activity", 
                "file-event": "file-activity",
                "registry-event": "registry-activity",
                "authentication": "auth-activity",
                "firewall-activity": "network-activity",
                "dns-query": "dns-activity",
                "endpoint-login": "endpoint-login-activity"
            }
            return family_mapping.get(activity, "General Activity")
        
        return "General Activity"

    def _get_valid_rule_group_id(self, family_id: str) -> str:
        """Map family ID to valid rule group ID, fallback to ga-ti-group"""
        family_to_group_mapping = {
            "process-creation-activity": "pc-susp-command-group",
            "network-activity": "network-connection-group",
            "file-activity": "file-modification-group", 
            "registry-activity": "registry-modification-group",
            "auth-activity": "auth-failure-group",
            "dns-activity": "dns-query-group",
            "endpoint-login-activity": "endpoint-login-failure-group",
            "General Activity": "ga-ti-group"
        }
        return family_to_group_mapping.get(family_id, "ga-ti-group")

    def _get_mitre_technique_info(self, technique_key: str) -> dict:
        """Map MITRE technique ID to technique name and tactic using Uncoder's dictionaries"""
        try:
            # Load techniques dictionary - use absolute path from container root
            techniques_path = "/siem_converter/app/dictionaries/techniques.json"
            
            with open(techniques_path, 'r') as f:
                techniques = json.load(f)
            
            # Load tactics dictionary
            tactics_path = "/siem_converter/app/dictionaries/tactics.json"
            with open(tactics_path, 'r') as f:
                tactics = json.load(f)
            
            # Look up technique by ID (e.g., t1059 or T1059)
            technique_data = techniques.get(technique_key.lower())
            if technique_data:
                # Get first tactic for this technique
                tactic_name = technique_data.get("tactic", ["Execution"])[0]
                
                # Find tactic ID from tactics dictionary
                tactic_key = None
                for tactic_id, tactic_info in tactics.items():
                    if tactic_info.get("tactic") == tactic_name:
                        tactic_key = tactic_info.get("external_id")
                        break
                
                return {
                    "techniqueKey": technique_key,
                    "technique": technique_data.get("technique", technique_key),
                    "tactic": tactic_name,
                    "tacticKey": tactic_key or "TA0002"  # Default to Execution
                }
        except Exception as e:
            print(f"Error loading MITRE data: {e}")
        
        return None


@render_manager.register
class ExabeamCorrelationRuleRender(PlatformQueryRender):
    details: PlatformDetails = exabeam_correlation_rule_details
    mappings: ExabeamMappings = ExabeamMappings(
        platform_dir="exabeam", platform_details=exabeam_correlation_rule_details
    )

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_render = ExabeamEQLFieldValueRender(or_token=or_token)
    comment_symbol = "//"

    def generate_prefix(self, log_source_signature: dict, functions_prefix: str = "") -> str:
        return ""

    def wrap_with_comment(self, content: str) -> str:
        return f"// {content}"

    def finalize_query(
        self,
        prefix: str,
        query: str,
        functions: str,
        meta_info: dict = None,
        source_mapping: dict = None,
        not_supported_functions: list = None,
        unmapped_fields: list = None,
        *args,
        **kwargs,
    ) -> str:
        import copy
        rule = copy.deepcopy(EXABEAM_CORRELATION_RULE_TEMPLATE)
        
        # Get the rule definition object
        rule_def = rule["ruleDefinitions"][0]
        sequence = rule_def["sequencesConfig"]["sequences"][0]
        
        # Set basic rule info
        rule_def["name"] = getattr(meta_info, 'title', None) or "Uncoder Generated Correlation Rule"
        rule_def["description"] = getattr(meta_info, 'description', None) or f"Correlation rule generated from rule translation"
        
        # Map severity
        if meta_info and hasattr(meta_info, 'severity'):
            severity_map = {
                "low": "low",
                "medium": "medium", 
                "high": "high",
                "critical": "critical"
            }
            rule_def["severity"] = severity_map.get(str(meta_info.severity).lower(), "medium")
        
        # Extract MITRE mapping if available
        if meta_info and hasattr(meta_info, 'tags') and meta_info.tags:
            mitre_tags = [tag for tag in meta_info.tags if tag.startswith("attack.")]
            if mitre_tags:
                mitre_mappings = []
                for tag in mitre_tags:
                    technique_key = tag.replace("attack.", "").upper()
                    if technique_key.startswith("T"):
                        technique_info = self._get_mitre_technique_info(technique_key)
                        if technique_info:
                            mitre_mappings.append(technique_info)
                
                if mitre_mappings:
                    rule_def["mitre"] = mitre_mappings[:3]  # Limit to 3 MITRE techniques
        
        # Set use case (single string, not array)
        use_cases = self._infer_use_cases(query, meta_info)
        rule_def["useCase"] = use_cases[0].lower() if use_cases else "malware"
        
        # Set sequence details
        sequence["query"] = query
        sequence["id"] = str(uuid.uuid4())
        sequence["name"] = ""
        
        if not_supported_functions:
            rule_def["description"] += f" Note: Unsupported functions: {', '.join(not_supported_functions)}"
        
        if unmapped_fields:
            rule_def["description"] += f" Note: Unmapped fields: {', '.join(unmapped_fields)}"
        
        return json.dumps(rule, indent=2)

    def _get_mitre_technique_info(self, technique_key: str) -> dict:
        """Get MITRE technique information from Uncoder's dictionaries"""
        try:
            techniques_path = "/siem_converter/app/dictionaries/techniques.json"
            with open(techniques_path, 'r') as f:
                techniques = json.load(f)
            
            tactics_path = "/siem_converter/app/dictionaries/tactics.json"
            with open(tactics_path, 'r') as f:
                tactics = json.load(f)
            
            # Find the technique
            for technique_data in techniques:
                if technique_data.get("technique") == technique_key:
                    # Get the first tactic for this technique
                    technique_tactics = technique_data.get("tactics", [])
                    if technique_tactics:
                        tactic_key = technique_tactics[0]
                        # Find tactic name
                        tactic_name = "Execution"  # Default
                        for tactic_data in tactics:
                            if tactic_data.get("tactic") == tactic_key:
                                tactic_name = tactic_data.get("name", "Execution")
                                break
                        
                        return {
                            "techniqueKey": technique_key,
                            "technique": technique_data.get("technique", technique_key),
                            "tactic": tactic_name,
                            "tacticKey": tactic_key or "TA0002"  # Default to Execution
                        }
        except Exception as e:
            print(f"Error loading MITRE data: {e}")
        
        return None

    def _map_category_to_activity(self, category: str) -> str:
        category_mapping = {
            "process_creation": "process-create",
            "network_connection": "network-connection",
            "file_event": "file-event", 
            "registry_event": "registry-event",
            "authentication": "authentication",
            "firewall": "firewall-activity",
        }
        return category_mapping.get(category, "process-create")

    def _infer_use_cases(self, query: str, meta_info) -> list:
        query_lower = query.lower()
        use_cases = []
        
        # Check for specific attack patterns in query
        if any(term in query_lower for term in ["password", "credential", "auth", "login"]):
            use_cases.append("Compromised Credentials")
        if any(term in query_lower for term in ["privilege", "admin", "elevated", "system"]):
            use_cases.append("Privilege Escalation")
        if any(term in query_lower for term in ["malware", "virus", "trojan", "backdoor"]):
            use_cases.append("Malware")
        if any(term in query_lower for term in ["exfil", "data", "transfer", "download"]):
            use_cases.append("Data Exfiltration")
        
        # Check meta_info tags for use case hints
        if meta_info and hasattr(meta_info, 'tags') and meta_info.tags:
            for tag in meta_info.tags:
                if "evasion" in tag.lower():
                    use_cases.append("Evasion")
                elif "execution" in tag.lower():
                    use_cases.append("Abnormal Process Execution")
                elif "initial-access" in tag.lower():
                    use_cases.append("Remote Code Execution")
        
        return use_cases or ["Malware"]