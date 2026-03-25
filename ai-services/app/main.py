import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.sign import router as sign_router
from app.api.stt import router as stt_router
from app.api.tts import router as tts_router
from app.core.logging_middleware import RequestLoggingMiddleware

app = FastAPI(title='Multimodal AI Services', version='1.0.0')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(stt_router)
app.include_router(tts_router)
app.include_router(sign_router)


@app.get('/health')
async def health():
    return {'status': 'ok'}
