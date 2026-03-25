from rest_framework.routers import DefaultRouter

from .views import MessageViewSet, SessionViewSet

router = DefaultRouter()
router.register('sessions', SessionViewSet, basename='chat-session')
router.register('messages', MessageViewSet, basename='chat-message')

urlpatterns = router.urls
