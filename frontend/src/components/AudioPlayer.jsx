import { aiApi } from '../services/api';
import { useTranslation } from 'react-i18next';

export default function AudioPlayer({ text }) {
  const { t } = useTranslation();

  const handleSpeak = async () => {
    if (!text) return;
    const response = await aiApi.synthesizeSpeech({ text });
    const url = URL.createObjectURL(response.data);
    const audio = new Audio(url);
    audio.play();
  };

  return (
    <section className="rounded-2xl bg-white/90 p-4 shadow-xl">
      <h2 className="font-heading text-xl font-bold text-slate-900">{t('textToSpeech')}</h2>
      <button
        className="mt-3 rounded-lg bg-mint px-5 py-3 text-lg font-semibold text-white disabled:opacity-40"
        disabled={!text}
        onClick={handleSpeak}
      >
        {t('playLatest')}
      </button>
    </section>
  );
}
