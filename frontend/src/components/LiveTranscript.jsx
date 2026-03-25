import { useTranslation } from 'react-i18next';

export default function LiveTranscript({ transcript }) {
  const { t } = useTranslation();

  return (
    <section className="rounded-2xl bg-white/90 p-4 shadow-xl">
      <h2 className="font-heading text-xl font-bold text-slate-900">{t('liveTranscript')}</h2>
      <p className="mt-3 min-h-20 rounded-xl border border-slate-200 bg-slate-50 p-4 text-xl leading-relaxed text-slate-900">
        {transcript || t('transcriptHint')}
      </p>
    </section>
  );
}
