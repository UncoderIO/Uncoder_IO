from os.path import abspath, dirname
from typing import Union, List

APP_PATH = dirname(abspath(__file__))

CTI_MIN_LIMIT_QUERY = 10000

DEFAULT_VALUE_TYPE = Union[Union[int, str, List[int], List[str]]]
