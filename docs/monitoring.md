# Logging and Monitoring

## Backend

- Structured console logging configured via Django `LOGGING`.
- Request-level errors are emitted from `django.request` logger.
- App domain logs can be emitted using `logging.getLogger('apps')`.

## AI Services

- FastAPI middleware captures method/path/status/latency.
- Unhandled exceptions are logged with stack traces.

## Production Recommendations

1. Ship logs to centralized sink (Datadog, ELK, or Azure Monitor).
2. Add uptime monitors for `/health` and websocket handshake endpoint.
3. Configure alerts for 5xx spikes and websocket disconnect anomalies.
