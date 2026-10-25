import { useState, useEffect } from 'react';
import { ChevronLeft, Signal } from 'lucide-react';

export default function LockScreen({ onUnlock, onBack }) {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const months = [
    'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
    'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
  ];
  const days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'];

  const timeStr = time.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
  const dateStr = `${days[time.getDay()]}, ${time.getDate()} ${months[time.getMonth()]}`;

  return (
    <div className="relative w-full h-full text-white font-sans flex flex-col justify-between p-4 overflow-hidden">

      {/* Обои */}
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: "url('/wallpaper.jpg')" }}
      />
      {/* Затемнение для читаемости */}
      <div className="absolute inset-0 bg-black/40" />

      {/* Статус-бар */}
      <div className="relative z-10 flex justify-between text-xs font-medium px-2 mb-4 text-white drop-shadow">
        <span>{timeStr}</span>
        <div className="flex gap-1.5 items-center">
          <Signal size={14} />
          <span>📡</span>
          <div className="flex items-center gap-1">
            <svg width="18" height="11" viewBox="0 0 18 11">
              <rect x="0.5" y="0.5" width="14" height="10" rx="2" stroke="white" strokeWidth="0.8" fill="none" />
              <rect x="2" y="2" width="10" height="7" rx="1" fill="white" />
              <rect x="15.5" y="3.5" width="1.5" height="4" rx="0.5" fill="white" />
            </svg>
            <span className="text-[10px]">12</span>
          </div>
        </div>
      </div>

      {/* Часы, дата, погода */}
      <div className="relative z-10 flex-1 flex flex-col items-center justify-center">
        <div className="text-9xl font-light leading-none mb-2 text-white drop-shadow-lg" style={{ letterSpacing: '-2px' }}>
          {timeStr}
        </div>
        <div className="text-base text-white/80 mt-2 font-normal drop-shadow">
          {dateStr}
        </div>
        <div className="flex items-center gap-2 mt-4 text-sm text-white/80 drop-shadow">
          <span className="text-2xl">🌥️</span>
          <span>+7°  Москва</span>
        </div>
      </div>

      {/* Карточка уведомления */}
      <div className="relative z-10 flex items-center gap-3 bg-zinc-900/70 backdrop-blur-md rounded-2xl p-3 mb-6 border border-white/10">
        <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-lg flex-shrink-0">
          💬
        </div>
        <div className="flex flex-col">
          <div className="text-sm font-semibold text-white">Сообщения</div>
          <div className="text-xs text-zinc-300">1 новое сообщение</div>
        </div>
      </div>

      {/* Кнопка разблокировки */}
      <button
        onClick={onUnlock}
        className="relative z-10 py-4 px-4 bg-transparent text-white/70 text-sm font-normal hover:text-white transition-colors active:opacity-70 drop-shadow"
      >
        ▲  Смахните, чтобы разблокировать
      </button>
    </div>
  );
}