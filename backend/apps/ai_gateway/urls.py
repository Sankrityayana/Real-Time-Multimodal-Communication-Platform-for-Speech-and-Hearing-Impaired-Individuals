from django.urls import path

from .views import DetectSignView, TextToSpeechView, TranscribeAudioView

urlpatterns = [
    path('transcribe/', TranscribeAudioView.as_view(), name='ai-transcribe'),
    path('tts/', TextToSpeechView.as_view(), name='ai-tts'),
    path('sign/detect/', DetectSignView.as_view(), name='ai-sign-detect')
]
