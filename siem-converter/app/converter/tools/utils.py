import re
from typing import Optional, List


def get_match_group(match: re.Match, group_name: str) -> Optional[str]:
    try:
        return match.group(group_name)
    except IndexError:
        return


def concatenate_str(str1: str, str2: str) -> str:
    return str1 + " " + str2 if str1 else str2


def get_mitre_attack_str(mitre_attack: List[str]) -> str:
    return f"MITRE ATT&CK: {', '.join(mitre_attack).upper()}." if mitre_attack else ""


def get_author_str(author: str) -> str:
    return f"Author: {author}." if author else ""


def get_licence_str(licence: str) -> str:
    return f"Licence: {licence}."


def get_rule_id_str(rule_id: str) -> str:
    return f"Rule ID: {rule_id}."


def get_references_str(references: List[str]) -> str:
    return f"References: {', '.join(references)}." if references else ""
