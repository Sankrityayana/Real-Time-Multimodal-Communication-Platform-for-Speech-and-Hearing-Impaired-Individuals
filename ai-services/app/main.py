from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.stt import router as stt_router
from app.api.tts import router as tts_router

app = FastAPI(title='Multimodal AI Services', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(stt_router)
app.include_router(tts_router)


@app.get('/health')
async def health():
    return {'status': 'ok'}
