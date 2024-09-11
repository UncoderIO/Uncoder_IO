import os.path

from app.translator.core.functions import PlatformFunctions
from app.translator.platforms.palo_alto.functions.manager import CortexXQLFunctionsManager, cortex_xql_functions_manager


class CortexXQLFunctions(PlatformFunctions):
    dir_path: str = os.path.abspath(os.path.dirname(__file__))
    manager: CortexXQLFunctionsManager = cortex_xql_functions_manager


cortex_xql_functions = CortexXQLFunctions()
