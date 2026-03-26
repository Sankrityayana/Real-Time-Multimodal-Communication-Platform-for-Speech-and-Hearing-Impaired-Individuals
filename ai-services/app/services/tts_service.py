import os
from tempfile import mkstemp

import pyttsx3


def _select_voice(engine, lang: str):
    target = lang.lower()
    for voice in engine.getProperty('voices'):
        languages = getattr(voice, 'languages', [])
        language_text = ' '.join(
            item.decode(errors='ignore') if isinstance(item, bytes) else str(item)
            for item in languages
        ).lower()

        if target in language_text:
            engine.setProperty('voice', voice.id)
            return


def synthesize_text_to_wav(text: str, lang: str = 'en') -> bytes:
    engine = pyttsx3.init()
    _select_voice(engine, lang)

    fd, tmp_path = mkstemp(suffix='.wav')
    os.close(fd)
    try:
        engine.save_to_file(text, tmp_path)
        engine.runAndWait()

        with open(tmp_path, 'rb') as audio_file:
            return audio_file.read()
    finally:
        engine.stop()
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
