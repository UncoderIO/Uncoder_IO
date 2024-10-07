from fastapi import APIRouter, Body

from app.models.translation import InfoMessage, OneTranslationData, Platform, TranslatorPlatforms
from app.translator.core.context_vars import return_only_first_query_ctx_var
from app.translator.cti_translator import CTITranslator
from app.translator.translator import app_translator

st_router = APIRouter()


@st_router.post("/translate", tags=["translator"], description="Generate target translation")
@st_router.post("/translate/", include_in_schema=False)
def translate_one(
    source_platform_id: str = Body(..., embed=True),
    target_platform_id: str = Body(..., embed=True),
    text: str = Body(..., embed=True),
    return_only_first_query: bool = False,
) -> OneTranslationData:
    return_only_first_query_ctx_var.set(return_only_first_query)
    status, data = app_translator.translate_one(text=text, source=source_platform_id, target=target_platform_id)
    if status:
        return OneTranslationData(status=status, translation=data, target_platform_id=target_platform_id)

    info_message = InfoMessage(message=data, severity="error")
    return OneTranslationData(info=info_message, status=status, target_platform_id=target_platform_id)


@st_router.post("/translate/all", tags=["translator"], description="Generate all translations")
@st_router.post("/translate/all/", include_in_schema=False)
def translate_all(
    source_platform_id: str = Body(..., embed=True),
    text: str = Body(..., embed=True),
    return_only_first_query: bool = False,
) -> list[OneTranslationData]:
    return_only_first_query_ctx_var.set(return_only_first_query)
    result = app_translator.translate_all(text=text, source=source_platform_id)
    translations = []
    for platform_result in result:
        if platform_result.get("status"):
            translations.append(
                OneTranslationData(
                    status=platform_result.get("status", True),
                    translation=platform_result.get("result"),
                    target_platform_id=platform_result.get("platform_id"),
                )
            )
        else:
            translations.append(
                OneTranslationData(
                    status=platform_result.get("status", False),
                    info=InfoMessage(message=platform_result.get("result"), severity="error"),
                    target_platform_id=platform_result.get("platform_id"),
                )
            )
    return translations


@st_router.get("/platforms", tags=["translator"], description="Get translator platforms")
@st_router.get("/platforms/", include_in_schema=False)
def get_translator_platforms() -> TranslatorPlatforms:
    renders, parsers = app_translator.get_all_platforms()
    return TranslatorPlatforms(renders=renders, parsers=parsers)


@st_router.get("/all_platforms", description="Get Sigma, RootA and iocs platforms")
@st_router.get("/all_platforms/", include_in_schema=False)
def get_all_platforms() -> list:
    translator_renders, translator_parsers = app_translator.get_all_platforms()
    return [
        Platform(
            id="roota",
            name="RootA",
            code="roota",
            group_name="RootA",
            group_id="roota",
            renders=translator_renders,
            parsers=translator_parsers,
        ),
        Platform(
            id="sigma",
            name="Sigma",
            code="sigma",
            group_name="Sigma",
            group_id="sigma",
            renders=[render for render in translator_renders if render.code != "sigma"],
        ),
        Platform(
            id="ioc", name="IOCs", code="ioc", group_name="IOCs", group_id="ioc", renders=CTITranslator().get_renders()
        ),
    ]
