from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ai_service_port: int = 8100
    stt_model_path: str = 'models/vosk-model-small-en-us-0.15'
    tts_provider: str = 'pyttsx3'
    enable_gpu: bool = False

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


settings = Settings()
