from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.stt_service import transcribe_audio_bytes

router = APIRouter(prefix='/stt', tags=['speech-to-text'])


@router.post('/transcribe')
async def transcribe(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail='audio file is required')

    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail='empty file')

    return transcribe_audio_bytes(audio_bytes)
