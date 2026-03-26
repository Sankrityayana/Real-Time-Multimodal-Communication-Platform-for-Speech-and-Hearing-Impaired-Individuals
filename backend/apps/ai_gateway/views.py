from django.conf import settings
from django.http import HttpResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from apps.chat.models import Message, Session
from apps.chat.serializers import MessageSerializer
from .serializers import SignPayloadSerializer, TextPayloadSerializer


class TranscribeAudioView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'detail': 'file is required'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        session_id = request.data.get('session_id')
        response = requests.post(
            f'{settings.AI_SERVICE_BASE_URL}/stt/transcribe',
            files={'file': (file.name, file.read(), file.content_type or 'audio/webm')},
            timeout=30
        )

        data = response.json()
        text = data.get('text', '').strip()
        if text and session_id:
            self._save_and_broadcast(session_id, request.user.id, text, 'speech')

        return Response(data, status=response.status_code)

    def _save_and_broadcast(self, session_id, user_id, content, modality):
        try:
            session = Session.objects.get(id=session_id, created_by_id=user_id, is_active=True)
        except Session.DoesNotExist:
            return

        message = Message.objects.create(
            session=session,
            sender_id=user_id,
            content=content,
            modality=modality
        )

        payload = {
            'type': 'message',
            'data': MessageSerializer(message).data
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{session_id}',
            {
                'type': 'chat.message',
                'payload': payload
            }
        )


class TextToSpeechView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TextPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = requests.post(
            f'{settings.AI_SERVICE_BASE_URL}/tts/synthesize',
            json=serializer.validated_data,
            timeout=30
        )
        if response.status_code >= 400:
            try:
                return Response(response.json(), status=response.status_code)
            except ValueError:
                return Response({'detail': 'TTS service failed'}, status=response.status_code)

        content_type = response.headers.get('Content-Type', 'audio/wav')
        return HttpResponse(response.content, content_type=content_type, status=response.status_code)


class DetectSignView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SignPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = requests.post(
            f'{settings.AI_SERVICE_BASE_URL}/sign/detect',
            json=serializer.validated_data,
            timeout=30
        )

        data = response.json()
        text = data.get('detected_text', '').strip()
        session_id = serializer.validated_data.get('session_id')
        if text and session_id:
            self._save_and_broadcast(session_id, request.user.id, text, 'sign')

        return Response(data, status=response.status_code)

    def _save_and_broadcast(self, session_id, user_id, content, modality):
        try:
            session = Session.objects.get(id=session_id, created_by_id=user_id, is_active=True)
        except Session.DoesNotExist:
            return

        message = Message.objects.create(
            session=session,
            sender_id=user_id,
            content=content,
            modality=modality
        )

        payload = {
            'type': 'message',
            'data': MessageSerializer(message).data
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{session_id}',
            {
                'type': 'chat.message',
                'payload': payload
            }
        )
