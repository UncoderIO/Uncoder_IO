from os.path import abspath, dirname
from typing import Union

from app.translator.core.str_value_manager import StrValue

APP_PATH = dirname(abspath(__file__))

CTI_MIN_LIMIT_QUERY = 10000

CTI_IOCS_PER_QUERY_LIMIT = 25

DEFAULT_VALUE_TYPE = Union[int, str, StrValue, list[Union[int, str, StrValue]]]
