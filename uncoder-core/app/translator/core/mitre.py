import json
import os
import ssl
import urllib.request
from json import JSONDecodeError
from typing import Optional, Union
from urllib.error import HTTPError

from app.translator.core.models.query_container import MitreInfoContainer, MitreTacticContainer, MitreTechniqueContainer
from app.translator.tools.singleton_meta import SingletonMeta
from const import ROOT_PROJECT_PATH


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.result = None


class Trie:
    """
    Trie (prefix tree) data structure for storing and searching Mitre ATT&CK Techniques and Tactics strings.

    This class handles the insertion and searching of strings related to Mitre ATT&CK Techniques and Tactics, even when
    the strings have variations in spacing, case, or underscores. By normalizing the text—converting it to lowercase and
    removing spaces and underscores—different variations of the same logical string are treated as equivalent.

    It means strings 'CredentialAccess', 'credential Access', and 'credential_access' will be processed identically,
    leading to the same result.
    """

    def __init__(self):
        self.root = TrieNode()

    def normalize_text(self, text: str) -> str:
        return text.replace(" ", "").lower().replace("_", "").lower()

    def insert(self, text: str, result: Union[MitreTacticContainer, MitreTechniqueContainer]) -> None:
        node = self.root
        normalized_text = self.normalize_text(text)

        for char in normalized_text:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end_of_word = True
        node.result = result


class TacticsTrie(Trie):
    def __init__(self):
        self.root = TrieNode()

    def search(self, text: str) -> Optional[MitreTacticContainer]:
        node: TrieNode = self.root
        normalized_text = self.normalize_text(text)

        for char in normalized_text:
            if char not in node.children:
                return
            node = node.children[char]

        if node.is_end_of_word:
            return node.result


class TechniquesTrie(Trie):
    def search(self, text: str) -> Optional[MitreTechniqueContainer]:
        node: TrieNode = self.root
        normalized_text = self.normalize_text(text)

        for char in normalized_text:
            if char not in node.children:
                return
            node = node.children[char]

        if node.is_end_of_word:
            return node.result


class MitreConfig(metaclass=SingletonMeta):
    config_url: str = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
    mitre_source_types: tuple = ("mitre-attack",)

    def __init__(self, server: bool = False):
        self.tactics: TacticsTrie = TacticsTrie()
        self.techniques: TechniquesTrie = TechniquesTrie()
        if not server:
            self.__load_mitre_configs_from_files()

    @staticmethod
    def __revoked_or_deprecated(entry: dict) -> bool:
        if entry.get("revoked") or entry.get("x_mitre_deprecated"):
            return True
        return False

    def __get_mitre_json(self) -> dict:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            with urllib.request.urlopen(self.config_url, context=ctx) as cti_json:
                return json.loads(cti_json.read().decode())
        except HTTPError:
            return {}

    def update_mitre_config(self) -> None:  # noqa: PLR0912
        if not (mitre_json := self.__get_mitre_json()):
            self.__load_mitre_configs_from_files()
            return

        tactic_map = {}

        # Map the tactics
        for entry in mitre_json["objects"]:
            if entry["type"] != "x-mitre-tactic" or self.__revoked_or_deprecated(entry):
                continue
            for ref in entry["external_references"]:
                if ref["source_name"] == "mitre-attack":
                    tactic_map[entry["x_mitre_shortname"]] = entry["name"]

                    tactic_data = MitreTacticContainer(
                        external_id=ref["external_id"], url=ref["url"], name=entry["name"]
                    )
                    self.tactics.insert(entry["name"], tactic_data)

                    break

        # Map the techniques
        for entry in mitre_json["objects"]:
            if entry["type"] != "attack-pattern" or self.__revoked_or_deprecated(entry):
                continue
            if entry.get("x_mitre_is_subtechnique"):
                continue
            for ref in entry["external_references"]:
                if ref["source_name"] in self.mitre_source_types:
                    sub_tactics = []
                    for tactic in entry["kill_chain_phases"]:
                        if tactic["kill_chain_name"] in self.mitre_source_types:
                            sub_tactics.append(tactic_map[tactic["phase_name"]])

                    technique_data = MitreTechniqueContainer(
                        technique_id=ref["external_id"], name=entry["name"], url=ref["url"], tactic=sub_tactics
                    )
                    self.techniques.insert(ref["external_id"], technique_data)
                    break

        # Map the sub-techniques
        for entry in mitre_json["objects"]:
            if entry["type"] != "attack-pattern" or self.__revoked_or_deprecated(entry):
                continue
            if entry.get("x_mitre_is_subtechnique"):
                for ref in entry["external_references"]:
                    if ref["source_name"] in self.mitre_source_types:
                        sub_technique_id = ref["external_id"]
                        sub_technique_name = entry["name"]
                        if parent_technique := self.techniques.search(sub_technique_id.split(".")[0]):
                            sub_technique_name = f"{parent_technique.name} : {sub_technique_name}"
                            sub_technique_data = MitreTechniqueContainer(
                                technique_id=ref["external_id"],
                                name=sub_technique_name,
                                url=ref["url"],
                                tactic=parent_technique.tactic,
                            )
                            self.techniques.insert(sub_technique_id, sub_technique_data)
                        break

    def __load_mitre_configs_from_files(self) -> None:
        try:
            with open(os.path.join(ROOT_PROJECT_PATH, "app/dictionaries/tactics.json")) as file:
                loaded = json.load(file)

                for tactic_name, tactic_data in loaded.items():
                    tactic = MitreTacticContainer(
                        external_id=tactic_data["external_id"], url=tactic_data["url"], name=tactic_data["tactic"]
                    )
                    self.tactics.insert(tactic_name, tactic)
        except JSONDecodeError:
            print("Unable to load MITRE Tactics")

        try:
            with open(os.path.join(ROOT_PROJECT_PATH, "app/dictionaries/techniques.json")) as file:
                loaded = json.load(file)
                for technique_id, technique_data in loaded.items():
                    technique = MitreTechniqueContainer(
                        technique_id=technique_data["technique_id"],
                        name=technique_data["technique"],
                        url=technique_data["url"],
                        tactic=technique_data["tactic"],
                    )
                    self.techniques.insert(technique_id, technique)
        except JSONDecodeError:
            print("Unable to load MITRE Techniques")

    def get_tactic(self, tactic: str) -> Optional[MitreTacticContainer]:
        return self.tactics.search(tactic)

    def get_technique(self, technique_id: str) -> Optional[MitreTechniqueContainer]:
        return self.techniques.search(technique_id)

    def get_mitre_info(
        self, tactics: Optional[list[str]] = None, techniques: Optional[list[str]] = None
    ) -> MitreInfoContainer:
        tactics_list = []
        techniques_list = []
        for tactic in tactics or []:
            if tactic_found := self.tactics.search(tactic):
                tactics_list.append(tactic_found)
        for technique in techniques or []:
            if technique_found := self.techniques.search(technique):
                techniques_list.append(technique_found)
        return MitreInfoContainer(
            tactics=sorted(tactics_list, key=lambda x: x.name),
            techniques=sorted(techniques_list, key=lambda x: x.technique_id),
        )
