from app.translator.core.functions import PlatformFunctions
from app.translator.platforms.palo_alto.functions.manager import CortexXQLFunctionsManager


class CortexXQLFunctions(PlatformFunctions):
    manager = CortexXQLFunctionsManager()


cortex_xql_functions = CortexXQLFunctions()
