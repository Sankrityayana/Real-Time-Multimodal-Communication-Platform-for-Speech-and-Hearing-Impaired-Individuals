# Real-Time Multimodal Communication Platform for Speech and Hearing Impaired Individuals

A production-ready full-stack platform enabling real-time communication through speech, text, and sign language for hearing, speech-impaired, and deaf users.

## Features

- Real-time chat over WebSockets (Django Channels, Redis optional)
- Speech-to-text (Whisper)
- Text-to-speech (gTTS)
- Sign gesture detection (OpenCV + MediaPipe)
- JWT authentication
- SQLite persistence for users, sessions, and messages
- PWA installability and basic offline cache
- English + Hindi localization

## Folder Structure

```text
project-root/
	frontend/
		public/
			manifest.webmanifest
			sw.js
		src/
			components/
			hooks/
			services/
			App.jsx
			i18n.js
			main.jsx
		.env.example
		package.json
		vercel.json
	backend/
		apps/
			accounts/
			chat/
			ai_gateway/
			core/
		config/
			settings.py
			asgi.py
			urls.py
			wsgi.py
		.env.example
		manage.py
		requirements.txt
		render.yaml
	ai-services/
		app/
			api/
			services/
			core/
			main.py
		.env.example
		requirements.txt
	docker/
		Dockerfile.frontend
		Dockerfile.backend
		Dockerfile.ai-services
		docker-compose.yml
		nginx.conf
	docs/
		deployment.md
		monitoring.md
		scaling.md
	.env.example
```

## Local Setup

### 1. Clone

```bash
git clone https://github.com/Sankrityayana/Real-Time-Multimodal-Communication-Platform-for-Speech-and-Hearing-Impaired-Individuals.git
cd Real-Time-Multimodal-Communication-Platform-for-Speech-and-Hearing-Impaired-Individuals
```

### 2. Backend

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### 3. AI Services

```bash
cd ai-services
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8100
```

### 4. Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

## Docker Run

```bash
cd docker
docker compose up --build
```

Services:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- AI Services: http://localhost:8100

## Core API Endpoints

- POST /api/auth/register/
- POST /api/auth/login/
- POST /api/auth/refresh/
- GET/POST /api/chat/sessions/
- GET /api/chat/sessions/{session_id}/messages/
- POST /api/ai/transcribe/
- POST /api/ai/tts/
- POST /api/ai/sign/detect/
- WS /ws/chat/{session_id}/?token={jwt}

## Environment Variables

### Root

- PROJECT_NAME
- JWT_SECRET

### Frontend (.env)

- VITE_API_BASE_URL
- VITE_WS_URL
- VITE_APP_NAME

### Backend (.env)

- DJANGO_SECRET_KEY
- DJANGO_DEBUG
- DJANGO_ALLOWED_HOSTS
- DATABASE_URL
- USE_REDIS
- REDIS_URL
- CORS_ALLOWED_ORIGINS
- AI_SERVICE_BASE_URL
- JWT_ACCESS_MINUTES
- JWT_REFRESH_DAYS

### AI Services (.env)

- AI_SERVICE_PORT
- OPENAI_API_KEY
- WHISPER_MODEL_SIZE
- TTS_PROVIDER
- ENABLE_GPU

## Deployment

- Frontend: Vercel using frontend/vercel.json
- Backend: Render/Railway using backend/render.yaml
- AI Services: Render/Railway/Fly with uvicorn start command
- Data: SQLite file (Redis optional for horizontal scale)

Detailed instructions: docs/deployment.md

## Testing

```bash
cd backend
python manage.py test
```

## Monitoring and Scaling

- Logging and alerts: docs/monitoring.md
- Redis/websocket scale strategy: docs/scaling.md
