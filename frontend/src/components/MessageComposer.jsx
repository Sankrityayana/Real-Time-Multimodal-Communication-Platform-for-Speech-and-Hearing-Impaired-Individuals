import { useState } from 'react';

export default function MessageComposer({ onSend }) {
  const [text, setText] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!text.trim()) return;
    onSend(text.trim());
    setText('');
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-2xl bg-white/90 p-4 shadow-xl">
      <label htmlFor="message" className="font-heading text-xl font-bold text-slate-900">
        Type Message
      </label>
      <div className="mt-3 flex flex-col gap-3 sm:flex-row">
        <textarea
          id="message"
          rows={3}
          value={text}
          onChange={(event) => setText(event.target.value)}
          className="w-full rounded-xl border border-slate-300 p-3 text-lg"
          placeholder="Type text to share..."
        />
        <button className="rounded-xl bg-slateblue px-6 py-3 text-lg font-semibold text-white" type="submit">
          Send
        </button>
      </div>
    </form>
  );
}
