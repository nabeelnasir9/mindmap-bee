from fastapi import APIRouter, HTTPException
from app.utils.localization import translate_text

router = APIRouter()


@router.get("/localization/languages")
async def get_available_languages():
    return {"languages": ["en", "es", "fr", "de"]}


@router.put("/localization/translate")
async def translate(content: str, target_language: str):
    try:
        translated_text = translate_text(content, target_language)
        return {"translated_text": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error translating text: {str(e)}")
