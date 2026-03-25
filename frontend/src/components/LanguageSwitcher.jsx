import { useTranslation } from 'react-i18next';

export default function LanguageSwitcher() {
  const { i18n } = useTranslation();

  return (
    <div className="mt-4 flex items-center gap-3">
      <label htmlFor="lang" className="text-sm font-semibold">Language</label>
      <select
        id="lang"
        className="rounded-lg border border-slate-300 bg-white px-3 py-2"
        value={i18n.language}
        onChange={(event) => i18n.changeLanguage(event.target.value)}
      >
        <option value="en">English</option>
        <option value="hi">Hindi</option>
      </select>
    </div>
  );
}
