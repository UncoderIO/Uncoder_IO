import json
import os
from collections.abc import Generator
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import APIRouter, FastAPI

from app.translator.core.mitre import MitreConfig
from const import ROOT_PROJECT_PATH

assistance_router = APIRouter()

suggestions = {}


@asynccontextmanager
async def lifespan(app: FastAPI) -> Generator[None, None, None]:  # noqa: ARG001
    MitreConfig().update_mitre_config()
    with open(os.path.join(ROOT_PROJECT_PATH, "app/dictionaries/uncoder_meta_info_roota.json")) as file:
        suggestions["roota"] = json.load(file)
    with open(os.path.join(ROOT_PROJECT_PATH, "app/dictionaries/uncoder_meta_info_sigma.json")) as file:
        suggestions["sigma"] = json.load(file)
    yield


@assistance_router.get("/suggestions/{parser_id}", tags=["assistance"], description="Get suggestions")
async def get_suggestions(parser_id: str) -> list[dict]:
    parser_dict = suggestions.get(parser_id, [])
    if parser_id == "roota":
        today = datetime.today().strftime("%Y-%m-%d")
        for i in parser_dict:
            if i["title"] == "Date":
                for v in i["dictionary"]:
                    v["name"] = today
                return parser_dict
    return parser_dict
