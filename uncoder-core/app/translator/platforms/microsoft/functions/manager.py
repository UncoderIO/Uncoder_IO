from app.translator.core.functions import PlatformFunctionsManager


class MicrosoftFunctionsManager(PlatformFunctionsManager):
    ...


microsoft_sentinel_functions_manager = MicrosoftFunctionsManager()
microsoft_defender_functions_manager = MicrosoftFunctionsManager()
