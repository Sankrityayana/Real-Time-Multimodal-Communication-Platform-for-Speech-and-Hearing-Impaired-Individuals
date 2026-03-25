# Scaling Notes

## Redis Channel Layer

- Backed by `channels_redis` with shared Redis endpoint.
- Tuned channel capacity and message expiry for bursty realtime traffic.
- Supports horizontal scale by running multiple Daphne workers.

## Realtime Scale Pattern

1. Deploy multiple backend instances.
2. Keep all instances connected to a shared Redis.
3. Route websocket traffic through a sticky-session capable ingress or managed websocket gateway.
