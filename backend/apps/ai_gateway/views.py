from django.conf import settings
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from .serializers import SignPayloadSerializer, TextPayloadSerializer


class TranscribeAudioView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'detail': 'file is required'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        response = requests.post(
            f'{settings.AI_SERVICE_BASE_URL}/stt/transcribe',
            files={'file': (file.name, file.read(), file.content_type or 'audio/webm')},
            timeout=30
        )
        return Response(response.json(), status=response.status_code)


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

        return HttpResponse(response.content, content_type='audio/mpeg', status=response.status_code)


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

        return Response(response.json(), status=response.status_code)
