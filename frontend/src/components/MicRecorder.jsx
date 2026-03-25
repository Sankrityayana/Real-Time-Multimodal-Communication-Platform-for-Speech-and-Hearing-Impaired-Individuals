import { aiApi } from '../services/api';

export default function MicRecorder({ recorder, onTranscript, sessionId }) {
  const handleTranscribe = async () => {
    if (!recorder.audioBlob) return;

    const formData = new FormData();
    formData.append('file', recorder.audioBlob, 'input.webm');
    formData.append('session_id', sessionId);

    const response = await aiApi.transcribeAudio(formData);
    onTranscript(response.data.text);
    recorder.setAudioBlob(null);
  };

  return (
    <section className="rounded-2xl bg-white/90 p-4 shadow-xl">
      <h2 className="font-heading text-xl font-bold text-slate-900">Microphone</h2>
      <div className="mt-3 flex flex-wrap gap-3">
        {!recorder.isRecording ? (
          <button
            className="rounded-lg bg-mint px-5 py-3 text-lg font-semibold text-white"
            onClick={recorder.startRecording}
          >
            Start Recording
          </button>
        ) : (
          <button
            className="rounded-lg bg-rose px-5 py-3 text-lg font-semibold text-white"
            onClick={recorder.stopRecording}
          >
            Stop Recording
          </button>
        )}
        <button
          className="rounded-lg bg-slate-800 px-5 py-3 text-lg font-semibold text-white disabled:opacity-40"
          disabled={!recorder.audioBlob || !sessionId}
          onClick={handleTranscribe}
        >
          Transcribe
        </button>
      </div>
    </section>
  );
}
