import datetime
import json
from datetime import datetime
from typing import List, Dict
import os

from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from const import ROOT_PROJECT_PATH


assistance_router = APIRouter()

suggestions = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    with open(os.path.join(ROOT_PROJECT_PATH, 'app/dictionaries/uncoder_meta_info_roota.json'), 'r') as file:
        json_f = json.load(file)
        suggestions['roota'] = json_f
    with open(os.path.join(ROOT_PROJECT_PATH, 'app/dictionaries/uncoder_meta_info_sigma.json'), 'r') as file:
        json_f = json.load(file)
        suggestions['sigma'] = json_f
    yield


@assistance_router.get(
    '/suggestions/{parser_id}',
    tags=["assistance"],
    description="Get suggestions"
)
async def get_suggestions(parser_id: str) -> List[Dict]:
    parser_dict = suggestions.get(parser_id, [])
    if parser_id == 'roota':
        today = datetime.today().strftime('%Y-%m-%d')
        for i in parser_dict:
            if i['title'] == 'Date':
                for v in i['dictionary']:
                    v['name'] = today
                return parser_dict
    return parser_dict
