from fastapi import APIRouter, Body

from app.translator.translator import SiemConverter
from app.translator.cti_translator import CTIConverter
from app.models.translation import OneTranslationData, ConvertorPlatforms, Platform, InfoMessage

st_router = APIRouter()

converter = SiemConverter()


@st_router.post(
    "/translate",
    tags=["siem_translate"],
    description="Generate target translation",
)
@st_router.post("/translate/", include_in_schema=False)
def generate_one_translation(
    source_siem: str = Body(..., embed=True),
    source_scheme: str = Body(None, embed=True),
    target_siem: str = Body(..., embed=True),
    target_scheme: str = Body(None, embed=True),
    text: str = Body(..., embed=True),

) -> OneTranslationData:
    status, data = converter.generate_translation(
        text=text,
        source=source_siem,
        target=target_siem
    )
    if status:
        return OneTranslationData(
            status=status,
            translation=data,
            target_siem_type=target_siem)
    else:
        info_message = InfoMessage(message=data, severity="error")
        return OneTranslationData(
            info=info_message,
            status=status,
            target_siem_type=target_siem)


@st_router.post(
    "/translate/all",
    tags=["siem_translate"],
    description="Generate all translations",
)
@st_router.post("/translate/all/", include_in_schema=False)
def generate_all_translations(
    source_siem: str = Body(..., embed=True),
    source_scheme: str = Body(None, embed=True),
    text: str = Body(..., embed=True),
) -> list[OneTranslationData]:
    result = converter.generate_all_translation(
        text=text,
        source=source_siem
    )
    translations = []
    for siem_result in result:
        if siem_result.get("status"):
            translations.append(OneTranslationData(
                status=siem_result.get("status", True),
                translation=siem_result.get("result"),
                target_siem_type=siem_result.get("siem_type"))
            )
        else:
            translations.append(OneTranslationData(
                status=siem_result.get("status", False),
                info=InfoMessage(message=siem_result.get("result"), severity="error"),
                target_siem_type=siem_result.get("siem_type"))
            )
    return translations


@st_router.get(
    "/platforms",
    tags=["siem_translate"],
    description="Get translator platforms",
)
@st_router.get("/platforms/", include_in_schema=False)
def get_convertor_platforms() -> ConvertorPlatforms:
    renders, parsers = converter.get_all_platforms()
    return ConvertorPlatforms(renders=renders, parsers=parsers)


@st_router.get(
    "/all_platforms",
    description="Get Sigma, RootA and iocs platforms",
)
@st_router.get("/all_platforms/", include_in_schema=False)
def get_all_platforms() -> list:
    converter_renders, converter_platforms = converter.get_all_platforms()
    return [
        Platform(id="roota", name="RootA", code="roota", group_name="RootA", group_id="roota",
                 renders=converter_renders, parsers=converter_platforms),
        Platform(id="sigma", name="Sigma", code="sigma", group_name="Sigma", group_id="sigma",
                 renders=[render for render in converter_renders if render.code != "sigma"]),
        Platform(id="ioc", name="IOCs", code="ioc", group_name="IOCs", group_id="ioc",
                 renders=CTIConverter().get_renders())
    ]
