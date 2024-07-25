import importlib.util
import re
from contextlib import suppress
from typing import Optional, Union


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


def get_mitre_attack_str(mitre_attack: list[str]) -> str:
    return f"MITRE ATT&CK: {', '.join(mitre_attack).upper()}."


def get_author_str(author: str) -> str:
    return f"Author: {author}."


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
    author: Optional[str] = None,
    rule_id: Optional[str] = None,
    license_: Optional[str] = None,
    mitre_attack: Optional[Union[str, list[str]]] = None,
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
    rule_id: str = ""
    rule_author: str = ""
    rule_license: str = ""
    rule_references: list[str] = []

    rule_id_pattern = r"Rule ID:\s*([\w-]+)"
    author_pattern = r"Author:\s*([^\.]+)"
    license_pattern = r"License:\s*(.+?)\s"
    reference_pattern = r"Reference:\s*([^\s]+)"

    if rule_id_match := re.search(rule_id_pattern, description):
        rule_id = rule_id_match.group(1)
    if rule_author_match := re.search(author_pattern, description):
        rule_author = rule_author_match.group(1).strip()
    if rule_references_match := re.search(reference_pattern, description):
        rule_references = [rule_references_match.group(1)]
    if "License: DRL 1.1." in description:
        rule_license = "DRL 1.1."
    elif rule_license_match := re.search(license_pattern, description):
        rule_license = rule_license_match.group(1)
    description = re.sub(r"\s*(?:Author:|Rule ID:|License:|Reference:|$).*", "", description)

    return {
        "rule_id": rule_id,
        "rule_license": rule_license,
        "rule_description": description,
        "rule_author": rule_author,
        "rule_references": rule_references,
    }
