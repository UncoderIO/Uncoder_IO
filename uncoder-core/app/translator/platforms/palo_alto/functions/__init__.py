import os.path

from app.translator.core.functions import PlatformFunctions
from app.translator.platforms.palo_alto.functions.manager import (
    CortexXQLFunctionsManager,
    cortex_xdr_xql_functions_manager,
    cortex_xsiam_xql_functions_manager,
)


class CortexXQLFunctions(PlatformFunctions):
    dir_path: str = os.path.abspath(os.path.dirname(__file__))


class CortexXSIAMXQLFunctions(CortexXQLFunctions):
    manager: CortexXQLFunctionsManager = cortex_xsiam_xql_functions_manager


class CortexXDRXQLFunctions(CortexXQLFunctions):
    manager: CortexXQLFunctionsManager = cortex_xdr_xql_functions_manager


cortex_xsiam_xql_functions = CortexXSIAMXQLFunctions()
cortex_xdr_xql_functions = CortexXDRXQLFunctions()
