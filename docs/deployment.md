# Deployment Guide

## Frontend (Vercel)

1. Import repository in Vercel.
2. Set root directory to `frontend`.
3. Build command: `npm run build`.
4. Output directory: `dist`.
5. Environment variables:
   - `VITE_API_BASE_URL=https://<backend-domain>/api`
   - `VITE_WS_URL=wss://<backend-domain>/ws/chat/`

## Backend (Render/Railway)

1. Set root directory to `backend`.
2. Build command:
   `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
3. Start command:
   `daphne -b 0.0.0.0 -p $PORT config.asgi:application`
4. Required env vars:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=<backend-domain>`
   - `DATABASE_URL=sqlite:///db.sqlite3`
   - `REDIS_URL=<cloud-redis-url>`
   - `CORS_ALLOWED_ORIGINS=https://<frontend-domain>`
   - `AI_SERVICE_BASE_URL=https://<ai-service-domain>`

## AI Services (Render/Railway/Fly)

1. Root directory: `ai-services`.
2. Build command: `pip install -r requirements.txt`.
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Required env vars:
   - `WHISPER_MODEL_SIZE=base`
   - `ENABLE_GPU=False`

## Managed Data Services

- SQLite: Persist `db.sqlite3` on attached disk/volume.
- Redis: Use managed cloud Redis.

## Post Deploy Checks

1. Run backend health check: `GET /admin/` and `GET /api/auth/login/` (method not allowed expected).
2. Run AI health check: `GET /health`.
3. Open frontend and verify:
   - Login bootstrap works
   - Chat websocket connects
   - STT and TTS endpoints respond
