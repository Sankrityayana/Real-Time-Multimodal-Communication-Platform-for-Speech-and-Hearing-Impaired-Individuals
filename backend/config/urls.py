from django.http import JsonResponse
from django.contrib import admin
from django.urls import include, path


def health(_request):
    return JsonResponse({'status': 'ok', 'service': 'backend'})


urlpatterns = [
    path('', health),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/chat/', include('apps.chat.urls')),
    path('api/ai/', include('apps.ai_gateway.urls'))
]
