import { useEffect, useMemo, useRef, useState } from 'react';
import ChatPanel from './components/ChatPanel';
import MicRecorder from './components/MicRecorder';
import WebcamSignInput from './components/WebcamSignInput';
import LiveTranscript from './components/LiveTranscript';
import MessageComposer from './components/MessageComposer';
import AudioPlayer from './components/AudioPlayer';
import { authApi, setAuthToken } from './services/api';
import { createChatSocket } from './services/socket';
import { useAudioRecorder } from './hooks/useAudioRecorder';

const DEFAULT_CREDENTIALS = {
  email: 'demo@platform.com',
  password: 'Demo@12345',
  name: 'Demo User'
};

export default function App() {
  const [token, setToken] = useState('');
  const [messages, setMessages] = useState([]);
  const [transcript, setTranscript] = useState('');
  const sessionId = useMemo(() => crypto.randomUUID(), []);
  const socketRef = useRef(null);
  const recorder = useAudioRecorder();

  useEffect(() => {
    const bootstrapAuth = async () => {
      try {
        await authApi.register(DEFAULT_CREDENTIALS);
      } catch (error) {
        // User may already exist; login still proceeds.
      }

      const loginRes = await authApi.login({
        email: DEFAULT_CREDENTIALS.email,
        password: DEFAULT_CREDENTIALS.password
      });

      setToken(loginRes.data.access);
      setAuthToken(loginRes.data.access);
    };

    bootstrapAuth().catch((error) => console.error('Auth bootstrap failed', error));
  }, []);

  useEffect(() => {
    if (!token) return;

    const socket = createChatSocket(sessionId, token, (payload) => {
      if (payload.type === 'message') {
        setMessages((prev) => [...prev, payload.data]);
      }
      if (payload.type === 'transcription' || payload.type === 'sign_text') {
        setTranscript(payload.data.text);
      }
    });

    socketRef.current = socket;
    return () => socket.close();
  }, [sessionId, token]);

  const sendChatMessage = (content, modality = 'text') => {
    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) return;

    socketRef.current.send(
      JSON.stringify({
        action: 'send_message',
        payload: { content, modality }
      })
    );
  };

  const onTranscript = (text) => {
    setTranscript(text);
    sendChatMessage(text, 'speech');
  };

  const onSignDetected = (text) => {
    setTranscript(text);
    sendChatMessage(text, 'sign');
  };

  return (
    <main className="mx-auto max-w-7xl p-4 sm:p-8">
      <header className="rounded-3xl bg-slateblue p-6 text-white shadow-2xl">
        <h1 className="font-heading text-3xl font-bold sm:text-5xl">
          Real-Time Multimodal Communication Platform
        </h1>
        <p className="mt-2 text-lg sm:text-2xl">
          Accessible communication across speech, text, and sign language.
        </p>
      </header>

      <section className="mt-6 grid gap-6 lg:grid-cols-2">
        <MicRecorder recorder={recorder} onTranscript={onTranscript} />
        <WebcamSignInput onDetectedText={onSignDetected} />
        <LiveTranscript transcript={transcript} />
        <AudioPlayer text={messages[messages.length - 1]?.content || transcript} />
      </section>

      <section className="mt-6">
        <MessageComposer onSend={(text) => sendChatMessage(text, 'text')} />
      </section>

      <section className="mt-6">
        <ChatPanel messages={messages} />
      </section>
    </main>
  );
}
