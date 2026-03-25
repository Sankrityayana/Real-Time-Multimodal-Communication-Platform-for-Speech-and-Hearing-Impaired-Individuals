const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/chat/';

export const createChatSocket = (sessionId, token, onMessage) => {
  const url = `${WS_URL}${sessionId}/?token=${encodeURIComponent(token)}`;
  const socket = new WebSocket(url);

  socket.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data);
      onMessage(payload);
    } catch (error) {
      console.error('Invalid WebSocket payload', error);
    }
  };

  return socket;
};
