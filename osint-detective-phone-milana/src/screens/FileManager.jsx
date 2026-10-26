import { useState } from 'react';
import { ChevronLeft, FileText, Music, Video, Image, FileCode, X } from 'lucide-react';

const FILES = [
  {
    id: 'resume',
    name: 'Резюме_Миланы.pdf',
    Icon: FileText,
    color: 'bg-red-500',
    size: '234 КБ',
    date: '15.03.2025',
    status: 'ok',
    content:
      'РЕЗЮМЕ\nМилана Макарова\nМенеджер по работе с персоналом (HR)\nPRIME SYSTEMS\nОпыт: 5 лет\nПочта: milana.makarova@primesystems.io\nГод рождения: 1995',
  },
  {
    id: 'audio1',
    name: 'Запись_совещания_22.05.mp3',
    Icon: Music,
    color: 'bg-purple-500',
    size: '4.2 МБ',
    date: '22.05.2025',
    status: 'ok',
    content:
      '[ВОСПРОИЗВЕДЕНИЕ...]\n\n…— Я предупреждала, что так нельзя.\n— Ты понимаешь, что тебя просто используют?\n— Я всё задокументирую.\n\n[запись обрывается]',
  },
  {
    id: 'video1',
    name: 'Скрытая_запись_офис.mp4',
    Icon: Video,
    color: 'bg-pink-500',
    size: '128 МБ',
    date: '18.05.2025',
    status: 'corrupted',
  },
  {
    id: 'screenshot1',
    name: 'Screenshot_2025-05-20.png',
    Icon: Image,
    color: 'bg-blue-500',
    size: '182 КБ',
    date: '20.05.2025',
    status: 'ok',
    content:
      '[СКРИНШОТ ПЕРЕПИСКИ]\n\n@m_lebedeva_press: "Милана, я знаю про OD-17. Помоги мне разобраться."\nМилана: "Я расскажу тебе ВСЁ. Но никому больше."',
  },
  {
    id: 'screenshot2',
    name: 'Screenshot_2025-05-21.png',
    Icon: Image,
    color: 'bg-blue-500',
    size: '96 КБ',
    date: '21.05.2025',
    status: 'corrupted',
  },
  {
    id: 'note1',
    name: 'Заметки.txt',
    Icon: FileCode,
    color: 'bg-yellow-600',
    size: '2 КБ',
    date: '23.05.2025',
    status: 'ok',
    content:
      '— Лев предупредил, что Герман что-то подозревает\n— Они хотят встретиться в кафе в 13:00 (на фото геотег сохранился)\n— Не забыть забрать флешку из шкафчика',
  },
];

export default function FileManager({ onBack }) {
  const [openedFile, setOpenedFile] = useState(null);

  return (
    <div className="relative w-full h-full bg-zinc-950 text-white font-sans flex flex-col overflow-hidden">

      <div className="flex items-center gap-3 px-3 py-2.5 h-14 border-b border-zinc-800 flex-shrink-0">
        <button
          onClick={onBack}
          className="w-9 h-9 rounded-full hover:bg-zinc-800 flex items-center justify-center text-blue-500 transition-colors"
        >
          <ChevronLeft size={22} />
        </button>
        <div className="text-base font-semibold">Мои файлы</div>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        <div className="text-xs text-zinc-500 px-1 mb-1">Материалы дела №17 / MILANA</div>

        {FILES.map((file) => {
          const Icon = file.Icon;
          const corrupted = file.status === 'corrupted';
          return (
            <button
              key={file.id}
              onClick={() => setOpenedFile(file)}
              className={`w-full flex items-center gap-3 bg-zinc-900 rounded-2xl p-3 border transition-colors text-left active:scale-[0.98] ${
                corrupted ? 'border-red-900/60 opacity-70' : 'border-zinc-800 hover:bg-zinc-800'
              }`}
            >
              <div className={`w-11 h-11 ${file.color} rounded-xl flex items-center justify-center flex-shrink-0`}>
                <Icon size={22} className="text-white" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-semibold text-white truncate">{file.name}</div>
                <div className="text-xs text-zinc-500 mt-0.5">
                  {file.date} · {file.size}
                  {corrupted && <span className="text-red-400 ml-2">повреждён</span>}
                </div>
              </div>
            </button>
          );
        })}
      </div>

      <div className="bg-zinc-900 border-t border-zinc-800 p-3 text-center text-xs text-zinc-400">
        Часть файлов повреждена. Восстановлению не подлежат.
      </div>

      {openedFile && (
        <div
          className="absolute inset-0 z-[70] bg-black/90 flex flex-col items-center justify-center p-6"
          onClick={() => setOpenedFile(null)}
        >
          <button
            className="absolute top-4 right-4 text-white/70 hover:text-white"
            onClick={() => setOpenedFile(null)}
          >
            <X size={24} />
          </button>

          <div className="w-full max-w-sm">
            <div className="text-sm font-semibold mb-2">{openedFile.name}</div>
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 text-xs text-zinc-300 whitespace-pre-wrap leading-relaxed">
              {openedFile.status === 'corrupted'
                ? '⚠ Файл повреждён. Не удаётся открыть.\n\nВозможно, был перезаписан или удалён в процессе передачи.'
                : openedFile.content}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}