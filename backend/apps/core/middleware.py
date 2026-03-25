from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication


class QueryStringJWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query = parse_qs(scope.get('query_string', b'').decode())
        token = query.get('token', [None])[0]

        scope['user'] = await self._get_user(token)
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def _get_user(self, token):
        if not token:
            return AnonymousUser()

        jwt_auth = JWTAuthentication()
        try:
            validated = jwt_auth.get_validated_token(token)
            return jwt_auth.get_user(validated)
        except (InvalidToken, TokenError):
            return AnonymousUser()
