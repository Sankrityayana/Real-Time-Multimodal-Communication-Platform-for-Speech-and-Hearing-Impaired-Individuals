from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.services.tts_service import synthesize_text_to_mp3

router = APIRouter(prefix='/tts', tags=['text-to-speech'])


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    lang: str = Field(default='en', max_length=5)


@router.post('/synthesize')
async def synthesize(payload: TTSRequest):
    try:
        audio_bytes = synthesize_text_to_mp3(payload.text, payload.lang)
        return Response(content=audio_bytes, media_type='audio/mpeg')
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
