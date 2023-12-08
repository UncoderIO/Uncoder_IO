import re
from typing import Optional, List, Union


def get_match_group(match: re.Match, group_name: str) -> Optional[str]:
    try:
        return match.group(group_name)
    except IndexError:
        return


def concatenate_str(str1: str, str2: str) -> str:
    return str1 + " " + str2 if str1 else str2


def get_mitre_attack_str(mitre_attack: List[str]) -> str:
    return f"MITRE ATT&CK: {', '.join(mitre_attack).upper()}."


def get_author_str(author: str) -> str:
    return f"Author: {author}."


def get_license_str(license: str) -> str:
    license_str = f"License: {license}"
    if not license_str.endswith('.'):
        license_str += '.'
    return license_str

def get_description_str(description: str) -> str:
    if not description.endswith('.'):
        description += '.'
    return description

def get_rule_id_str(rule_id: str) -> str:
    return f"Rule ID: {rule_id}."


def get_references_str(references: List[str]) -> str:
    return f"References: {', '.join(references)}."

def get_rule_description_str(
        description: str,
        author: str = None,
        rule_id: str = None,
        license: str = None,
        mitre_attack: Union[str, list[str]] = None,
        references: str = None
) -> str:
    description_str = get_description_str(description)
    author_str = get_author_str(author) if author else None
    rule_id = get_rule_id_str(rule_id) if rule_id else None
    license_str = get_license_str(license) if license else None
    mitre_attack = get_mitre_attack_str(mitre_attack) if mitre_attack else None
    references = get_references_str(references) if references else None
    rule_description = description_str
    if author_str:
        rule_description = concatenate_str(rule_description, author_str)
    if rule_id:
        rule_description = concatenate_str(rule_description, rule_id)
    if license_str:
        rule_description = concatenate_str(rule_description, license_str)
    if mitre_attack:
        rule_description = concatenate_str(rule_description, mitre_attack)
    if references:
        rule_description = concatenate_str(rule_description, references)
    return rule_description
