# Scaling Notes

## Redis Channel Layer

- Optional: use `channels_redis` with shared Redis endpoint for multi-instance deployments.
- Local/default mode uses in-memory channel layer and does not need Redis.
- Redis mode supports horizontal scale by running multiple Daphne workers.

## Realtime Scale Pattern

1. Deploy multiple backend instances.
2. Keep all instances connected to a shared Redis.
3. Route websocket traffic through a sticky-session capable ingress or managed websocket gateway.
