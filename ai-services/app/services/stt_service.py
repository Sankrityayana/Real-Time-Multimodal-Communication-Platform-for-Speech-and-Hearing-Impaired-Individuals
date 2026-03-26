from functools import lru_cache
import json
import os
import subprocess
from tempfile import NamedTemporaryFile

from vosk import KaldiRecognizer, Model

from app.core.config import settings


@lru_cache(maxsize=1)
def get_whisper_model():
    model_path = settings.stt_model_path
    if not os.path.isdir(model_path):
        raise FileNotFoundError(
            f'Vosk model not found at {model_path}. Download a model from https://alphacephei.com/vosk/models and set STT_MODEL_PATH.'
        )
    return Model(model_path)


def _convert_to_wav(input_path: str, output_path: str):
    subprocess.run(
        [
            'ffmpeg',
            '-y',
            '-i',
            input_path,
            '-ar',
            '16000',
            '-ac',
            '1',
            '-f',
            'wav',
            output_path,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def transcribe_audio_bytes(audio_bytes: bytes):
    model = get_whisper_model()
    with NamedTemporaryFile(delete=True, suffix='.webm') as src, NamedTemporaryFile(delete=True, suffix='.wav') as wav:
        src.write(audio_bytes)
        src.flush()

        _convert_to_wav(src.name, wav.name)

        recognizer = KaldiRecognizer(model, 16000)
        recognizer.SetWords(True)

        with open(wav.name, 'rb') as audio_file:
            audio_file.read(44)
            while True:
                data = audio_file.read(4000)
                if len(data) == 0:
                    break
                recognizer.AcceptWaveform(data)

        final_result = json.loads(recognizer.FinalResult() or '{}')
        text = final_result.get('text', '').strip()

    return {
        'text': text,
        'language': 'en',
        'segments': []
    }
