from collections.abc import Callable

from app.translator.core.exceptions.core import BasePlatformException
from app.translator.core.exceptions.iocs import BaseIOCsException
from app.translator.core.exceptions.parser import BaseParserException
from app.translator.core.exceptions.render import BaseRenderException


def handle_translation_exceptions(func: Callable[..., ...]) -> Callable[..., tuple[bool, str]]:
    def exception_handler(*args, **kwargs) -> tuple[bool, str]:
        try:
            result = func(*args, **kwargs)
        except (BaseParserException, BasePlatformException, BaseRenderException, BaseIOCsException) as err:
            print(f"Unexpected error. {err!s}")
            return False, str(err)
        except Exception as err:
            print(f"Unexpected error. {err!s}")
            return False, "Unexpected error. To resolve it, please, contact us."
        else:
            if result:
                print("Translated successfully.")
                return True, result

            print("Unexpected error.")
            return False, "Unexpected error. To resolve it, please, contact us."

    return exception_handler
