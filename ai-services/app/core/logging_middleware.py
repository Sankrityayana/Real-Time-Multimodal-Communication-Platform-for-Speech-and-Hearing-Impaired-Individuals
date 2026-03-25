import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger('ai-services')


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        try:
            response = await call_next(request)
            duration = (time.perf_counter() - start) * 1000
            logger.info('%s %s %s %.2fms', request.method, request.url.path, response.status_code, duration)
            return response
        except Exception as exc:
            duration = (time.perf_counter() - start) * 1000
            logger.exception('Unhandled error in %s %s after %.2fms: %s', request.method, request.url.path, duration, exc)
            raise
