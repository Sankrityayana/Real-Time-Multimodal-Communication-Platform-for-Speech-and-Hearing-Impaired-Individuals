from functools import lru_cache
from tempfile import NamedTemporaryFile

import whisper

from app.core.config import settings


@lru_cache(maxsize=1)
def get_whisper_model():
    device = 'cuda' if settings.enable_gpu else 'cpu'
    return whisper.load_model(settings.whisper_model_size, device=device)


def transcribe_audio_bytes(audio_bytes: bytes):
    model = get_whisper_model()
    with NamedTemporaryFile(delete=True, suffix='.webm') as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        result = model.transcribe(tmp.name, fp16=settings.enable_gpu, task='transcribe')

    return {
        'text': result.get('text', '').strip(),
        'language': result.get('language', 'unknown'),
        'segments': result.get('segments', [])
    }
