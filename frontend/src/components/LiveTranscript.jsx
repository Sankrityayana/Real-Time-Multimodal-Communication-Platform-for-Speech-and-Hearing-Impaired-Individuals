export default function LiveTranscript({ transcript }) {
  return (
    <section className="rounded-2xl bg-white/90 p-4 shadow-xl">
      <h2 className="font-heading text-xl font-bold text-slate-900">Live Transcript</h2>
      <p className="mt-3 min-h-20 rounded-xl border border-slate-200 bg-slate-50 p-4 text-xl leading-relaxed text-slate-900">
        {transcript || 'Transcribed speech and detected signs appear here.'}
      </p>
    </section>
  );
}
