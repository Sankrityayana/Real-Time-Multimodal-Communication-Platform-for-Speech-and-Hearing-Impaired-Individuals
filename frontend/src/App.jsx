import { useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import ChatPanel from './components/ChatPanel';
import MicRecorder from './components/MicRecorder';
import WebcamSignInput from './components/WebcamSignInput';
import LiveTranscript from './components/LiveTranscript';
import MessageComposer from './components/MessageComposer';
import AudioPlayer from './components/AudioPlayer';
import LanguageSwitcher from './components/LanguageSwitcher';
import { authApi, chatApi, setAuthToken } from './services/api';
import { createChatSocket } from './services/socket';
import { useAudioRecorder } from './hooks/useAudioRecorder';

const DEFAULT_CREDENTIALS = {
  email: 'demo@platform.com',
  password: 'Demo@12345',
  name: 'Demo User'
};

export default function App() {
  const { t } = useTranslation();
  const [token, setToken] = useState('');
  const [messages, setMessages] = useState([]);
  const [transcript, setTranscript] = useState('');
  const [sessionId, setSessionId] = useState('');
  const socketRef = useRef(null);
  const recorder = useAudioRecorder();

  useEffect(() => {
    const bootstrapAuth = async () => {
      let loginRes;

      try {
        loginRes = await authApi.login({
          email: DEFAULT_CREDENTIALS.email,
          password: DEFAULT_CREDENTIALS.password
        });
      } catch (error) {
        await authApi.register(DEFAULT_CREDENTIALS);
        loginRes = await authApi.login({
          email: DEFAULT_CREDENTIALS.email,
          password: DEFAULT_CREDENTIALS.password
        });
      }

      setToken(loginRes.data.access);
      setAuthToken(loginRes.data.access);

      const sessionRes = await chatApi.createSession({});
      setSessionId(sessionRes.data.id);
    };

    bootstrapAuth().catch((error) => console.error('Auth bootstrap failed', error));
  }, []);

  useEffect(() => {
    if (!token || !sessionId) return;

    const socket = createChatSocket(sessionId, token, (payload) => {
      if (payload.type === 'message') {
        setMessages((prev) => [...prev, payload.data]);
      }
      if (payload.type === 'transcription' || payload.type === 'sign_text') {
        setTranscript(payload.data.text);
      }
    });

    socketRef.current = socket;
    return () => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
    };
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
  };

  const onSignDetected = (text) => {
    setTranscript(text);
  };

  return (
    <main className="mx-auto max-w-7xl p-4 sm:p-8">
      <header className="rounded-3xl bg-slateblue p-6 text-white shadow-2xl">
        <h1 className="font-heading text-3xl font-bold sm:text-5xl">
          {t('title')}
        </h1>
        <p className="mt-2 text-lg sm:text-2xl">
          {t('subtitle')}
        </p>
        <p className="mt-2 text-sm sm:text-base">Session: {sessionId || 'initializing...'}</p>
        <LanguageSwitcher />
      </header>

      <section className="mt-6 grid gap-6 lg:grid-cols-2">
        <MicRecorder recorder={recorder} onTranscript={onTranscript} sessionId={sessionId} />
        <WebcamSignInput onDetectedText={onSignDetected} sessionId={sessionId} />
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
