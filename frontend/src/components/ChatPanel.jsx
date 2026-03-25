import { useTranslation } from 'react-i18next';

export default function ChatPanel({ messages }) {
  const { t } = useTranslation();

  return (
    <section className="rounded-2xl bg-white/90 p-4 shadow-xl" aria-live="polite">
      <h2 className="font-heading text-2xl font-bold text-slate-900">{t('conversation')}</h2>
      <div className="mt-4 h-96 overflow-y-auto rounded-xl border border-slate-200 bg-slate-50 p-4">
        {messages.length === 0 && (
          <p className="text-lg text-slate-700">{t('noMessages')}</p>
        )}
        {messages.map((message) => (
          <article
            key={message.id}
            className="mb-3 rounded-lg border border-slate-200 bg-white p-3"
          >
            <p className="text-sm font-semibold uppercase tracking-wide text-slate-600">
              {message.sender} - {message.modality}
            </p>
            <p className="text-lg text-slate-900">{message.content}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
