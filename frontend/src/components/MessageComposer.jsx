import { useState } from 'react';
import { useTranslation } from 'react-i18next';

export default function MessageComposer({ onSend }) {
  const { t } = useTranslation();
  const [text, setText] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!text.trim()) return;
    onSend(text.trim());
    setText('');
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-2xl bg-white/90 p-4 shadow-xl">
      <label htmlFor="message" className="font-heading text-xl font-bold text-slate-900">{t('typeMessage')}</label>
      <div className="mt-3 flex flex-col gap-3 sm:flex-row">
        <textarea
          id="message"
          rows={3}
          value={text}
          onChange={(event) => setText(event.target.value)}
          className="w-full rounded-xl border border-slate-300 p-3 text-lg"
          placeholder={t('typePlaceholder')}
        />
        <button className="rounded-xl bg-slateblue px-6 py-3 text-lg font-semibold text-white" type="submit">
          {t('send')}
        </button>
      </div>
    </form>
  );
}
