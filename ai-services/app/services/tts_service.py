from io import BytesIO

from gtts import gTTS


def synthesize_text_to_mp3(text: str, lang: str = 'en') -> bytes:
    audio_buffer = BytesIO()
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer.read()
