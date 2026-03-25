import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from app.services.sign_service import detector

router = APIRouter(prefix='/sign', tags=['sign-language'])


class SignDetectRequest(BaseModel):
    image_base64: str


@router.post('/detect')
async def detect_sign(payload: SignDetectRequest):
    return detector.detect(payload.image_base64)


@router.websocket('/ws')
async def sign_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            image_base64 = payload.get('image_base64', '')
            result = detector.detect(image_base64)
            await websocket.send_text(json.dumps(result))
    except WebSocketDisconnect:
        return
