import json
import os
import ssl
import urllib.request
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Optional, Union
from urllib.error import HTTPError

from app.translator.tools.singleton_meta import SingletonMeta
from const import ROOT_PROJECT_PATH


@dataclass
class MitreTechniqueContainer:
    technique_id: str
    name: str
    url: str
    tactic: list[str]


@dataclass
class MitreTacticContainer:
    external_id: str
    url: str
    name: str


@dataclass
class MitreInfoContainer:
    tactics: Union[list[MitreTacticContainer], list]
    techniques: Union[list[MitreTechniqueContainer], list]


class MitreConfig(metaclass=SingletonMeta):
    config_url: str = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
    mitre_source_types: tuple = ("mitre-attack",)

    def __init__(self, server: bool = False):
        self.tactics = {}
        self.techniques = {}
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
        technique_map = {}

        # Map the tactics
        for entry in mitre_json["objects"]:
            if entry["type"] != "x-mitre-tactic" or self.__revoked_or_deprecated(entry):
                continue
            for ref in entry["external_references"]:
                if ref["source_name"] == "mitre-attack":
                    tactic_map[entry["x_mitre_shortname"]] = entry["name"]
                    self.tactics[entry["name"].replace(" ", "_").lower()] = {
                        "external_id": ref["external_id"],
                        "url": ref["url"],
                        "tactic": entry["name"],
                    }
                    break

        # Map the techniques
        for entry in mitre_json["objects"]:
            if entry["type"] != "attack-pattern" or self.__revoked_or_deprecated(entry):
                continue
            if entry.get("x_mitre_is_subtechnique"):
                continue
            for ref in entry["external_references"]:
                if ref["source_name"] in self.mitre_source_types:
                    technique_map[ref["external_id"]] = entry["name"]
                    sub_tactics = []
                    # Get Mitre Tactics (Kill-Chains)
                    for tactic in entry["kill_chain_phases"]:
                        if tactic["kill_chain_name"] in self.mitre_source_types:
                            # Map the short phase_name to tactic name
                            sub_tactics.append(tactic_map[tactic["phase_name"]])
                    self.techniques[ref["external_id"].lower()] = {
                        "technique_id": ref["external_id"],
                        "technique": entry["name"],
                        "url": ref["url"],
                        "tactic": sub_tactics,
                    }
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
                        parent_technique_name = technique_map[sub_technique_id.split(".")[0]]
                        parent_tactics = self.techniques.get(sub_technique_id.split(".")[0].lower(), {}).get(
                            "tactic", []
                        )
                        sub_technique_name = f"{parent_technique_name} : {sub_technique_name}"
                        self.techniques[ref["external_id"].lower()] = {
                            "technique_id": ref["external_id"],
                            "technique": sub_technique_name,
                            "url": ref["url"],
                            "tactic": parent_tactics,
                        }
                        break

    def __load_mitre_configs_from_files(self) -> None:
        try:
            with open(os.path.join(ROOT_PROJECT_PATH, "app/dictionaries/tactics.json")) as file:
                self.tactics = json.load(file)
        except JSONDecodeError:
            self.tactics = {}

        try:
            with open(os.path.join(ROOT_PROJECT_PATH, "app/dictionaries/techniques.json")) as file:
                self.techniques = json.load(file)
        except JSONDecodeError:
            self.techniques = {}

    def get_tactic(self, tactic: str) -> Optional[MitreTacticContainer]:
        tactic = tactic.replace(".", "_")
        if tactic_found := self.tactics.get(tactic):
            return MitreTacticContainer(
                external_id=tactic_found["external_id"], url=tactic_found["url"], name=tactic_found["tactic"]
            )

    def get_technique(self, technique_id: str) -> Optional[MitreTechniqueContainer]:
        if technique_found := self.techniques.get(technique_id):
            return MitreTechniqueContainer(
                technique_id=technique_found["technique_id"],
                name=technique_found["technique"],
                url=technique_found["url"],
                tactic=technique_found["tactic"],
            )

    def get_mitre_info(
        self, tactics: Optional[list[str]] = None, techniques: Optional[list[str]] = None
    ) -> Optional[MitreInfoContainer]:
        tactics_list = []
        techniques_list = []
        if tactics:
            for tactic in tactics:
                if tactic_found := self.get_tactic(tactic=tactic.lower()):
                    tactics_list.append(tactic_found)
        if techniques:
            for technique in techniques:
                if technique_found := self.get_technique(technique_id=technique.lower()):
                    techniques_list.append(technique_found)
        if tactics_list or techniques_list:
            return MitreInfoContainer(tactics=tactics_list, techniques=techniques_list)
