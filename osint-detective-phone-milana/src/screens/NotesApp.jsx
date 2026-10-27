import { useState } from 'react';
import { ChevronLeft, FileText } from 'lucide-react';
import SelfDestruct from '../components/SelfDestruct';

const NOTES = [
  {
    title: 'Список покупок',
    date: '20.10',
    body:
      '— молоко\n— хлеб\n— корм для Бони\n— зарядка от телефона',
  },
  {
    title: 'Личное',
    date: '15.10',
    body:
      'Лев злится, что скрываемся.\nЯ понимаю, что так нельзя — но если узнают, уволят обоих.\nЕще и этот Герман что-то вынюхивает вечно.\n Надо быть осторожнее...',
  },
  {
    title: 'CONNECT мой акк',
    date: '23.05',
    body:
      'Логин: makarova\nПароль: 1234',
  },
];

export default function NotesApp({ onBack }) {
  const [destroyed, setDestroyed] = useState({}); // { [index]: true }

  const handleFinish = (i) => {
    setDestroyed((d) => ({ ...d, [i]: true }));
  };

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex items-center gap-3 px-4 py-3 h-14 border-b border-zinc-800 flex-shrink-0">
        <button onClick={onBack} className="text-blue-500"><ChevronLeft size={24} /></button>
        <span className="text-sm font-semibold">Заметки</span>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {NOTES.map((n, i) => (
          <div key={i} className="bg-zinc-900 rounded-2xl p-4 border border-zinc-800">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <FileText size={14} className={n.selfDestruct ? 'text-red-500' : 'text-yellow-500'} />
                <span className="text-sm font-semibold text-white">{n.title}</span>
              </div>
              <span className="text-[10px] text-zinc-500">{n.date}</span>
            </div>

            {n.selfDestruct && !destroyed[i] ? (
              <SelfDestruct
                key="self"
                text={n.body}
                delay={3000}
                speed={45}
                onFinish={() => handleFinish(i)}
              />
            ) : n.selfDestruct && destroyed[i] ? (
              <div className="text-xs text-red-400/60 italic font-mono min-h-[100px] flex items-center justify-center border border-red-900/50 rounded-2xl p-4">
                [ файл удалён ]
              </div>
            ) : (
              <div className="text-xs text-zinc-400 whitespace-pre-wrap leading-relaxed">{n.body}</div>
            )}
          </div>
        ))}
      </div>

      <div className="bg-zinc-900 border-t border-zinc-800 p-3 text-center text-xs text-zinc-500">
        Обновлено: 20.10.2026
      </div>
    </div>
  );
}