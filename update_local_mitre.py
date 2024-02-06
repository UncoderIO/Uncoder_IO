import json
import os

from translator.app.translator.core.mitre import MitreConfig
from translator.const import ROOT_PROJECT_PATH

mitre_config = MitreConfig()
mitre_config.update_mitre_config()
with open(os.path.join(ROOT_PROJECT_PATH, "app/dictionaries/tactics.json"), "w") as file:
    json.dump(mitre_config.tactics, file, indent=4)

with open(os.path.join(ROOT_PROJECT_PATH, "app/dictionaries/techniques.json"), "w") as file:
    json.dump(mitre_config.techniques, file, indent=4)
