import importlib.util
import re
from contextlib import suppress
from typing import Optional


def execute_module(path: str) -> None:
    with suppress(FileNotFoundError):
        spec = importlib.util.spec_from_file_location("__init__", path)
        init_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(init_module)


def get_match_group(match: re.Match, group_name: str) -> Optional[str]:
    try:
        return match.group(group_name)
    except IndexError:
        return


def concatenate_str(str1: str, str2: str) -> str:
    return str1 + " " + str2 if str1 else str2


def get_mitre_attack_str(mitre_attack: list) -> str:
    return f"MITRE ATT&CK: {', '.join(mitre_attack).upper()}."


def get_author_str(author: list[str]) -> str:
    return f"Author: {', '.join(author)}."


def get_license_str(license_: str) -> str:
    license_str = f"License: {license_}"
    if not license_str.endswith("."):
        license_str += "."
    return license_str


def get_description_str(description: str) -> str:
    if description != "" and not description.endswith("."):
        description += "."
    return description


def get_rule_id_str(rule_id: str) -> str:
    return f"Rule ID: {rule_id}."


def get_references_str(references: list[str]) -> str:
    return f"References: {', '.join(references)}."


def get_rule_description_str(
    description: str,
    author: Optional[list[str]] = None,
    rule_id: Optional[str] = None,
    license_: Optional[str] = None,
    mitre_attack: Optional[list[str]] = None,
    references: Optional[list[str]] = None,
) -> str:
    rule_description = get_description_str(description)
    if author:
        rule_description = concatenate_str(rule_description, get_author_str(author))
    if rule_id:
        rule_description = concatenate_str(rule_description, get_rule_id_str(rule_id))
    if license_:
        rule_description = concatenate_str(rule_description, get_license_str(license_))
    if mitre_attack:
        rule_description = concatenate_str(rule_description, get_mitre_attack_str(mitre_attack))
    if references:
        rule_description = concatenate_str(rule_description, get_references_str(references))
    return rule_description


def parse_rule_description_str(description: str) -> dict:
    parsed = {}
    keys_map = {
        "references": "Reference",
        "mitre_attack": "MITRE ATT&CK",
        "license": "License",
        "rule_id": "Rule ID",
        "author": "Author",
    }
    pattern = r"___name___:\s*(?P<value>.+)\."
    for key, name in keys_map.items():
        if search := re.search(pattern.replace("___name___", name), description):
            if key in ("author", "references"):
                parsed[key] = [value.strip() for value in search.group("value").split(",")]
            else:
                parsed[key] = search.group("value")
            description = description[: search.start()]

    parsed["description"] = description.strip()
    return parsed
