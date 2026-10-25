import { Wifi, Bluetooth, Flashlight, Plane, BellOff, RotateCcw, Sun, Volume2, MessageSquare, ChevronUp } from 'lucide-react';

const TOGGLES = [
  { key: 'wifi', Icon: Wifi, label: 'Wi-Fi' },
  { key: 'bluetooth', Icon: Bluetooth, label: 'Bluetooth' },
  { key: 'flashlight', Icon: Flashlight, label: 'Фонарик' },
  { key: 'airplane', Icon: Plane, label: 'Полёт' },
  { key: 'dnd', Icon: BellOff, label: 'Не беспокоить' },
  { key: 'autoRotate', Icon: RotateCcw, label: 'Автоповорот' },
];

export default function NotificationShade({ open, onClose, settings, onToggle, onSlider, onOpenMessenger, hasUnread }) {
  return (
    <div
      className={`absolute inset-0 z-[60] transition-opacity duration-300 ${open ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}
    >
      {/* Затемнение под шторкой, клик закрывает */}
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />

      {/* Сама шторка */}
      <div
        className={`absolute top-0 left-0 right-0 bg-zinc-900/95 backdrop-blur-md rounded-b-[28px] shadow-2xl transition-transform duration-300 ease-out ${
          open ? 'translate-y-0' : '-translate-y-full'
        }`}
      >
        <div className="pt-8 pb-2 px-4">
          {/* Тумблеры */}
          <div className="grid grid-cols-3 gap-3 mb-4">
            {TOGGLES.map(({ key, Icon, label }) => {
              const active = settings[key];
              return (
                <button
                  key={key}
                  onClick={() => onToggle(key)}
                  className={`flex flex-col items-center justify-center gap-1.5 py-3 rounded-2xl transition-colors ${
                    active ? 'bg-blue-500 text-white' : 'bg-zinc-800 text-zinc-300'
                  }`}
                >
                  <Icon size={20} strokeWidth={1.8} />
                  <span className="text-[10px] leading-none text-center px-1">{label}</span>
                </button>
              );
            })}
          </div>

          {/* Яркость */}
          <div className="flex items-center gap-3 mb-3 bg-zinc-800 rounded-2xl px-4 py-2.5">
            <Sun size={16} className="text-zinc-400 flex-shrink-0" />
            <input
              type="range"
              min="0"
              max="100"
              value={settings.brightness}
              onChange={(e) => onSlider('brightness', Number(e.target.value))}
              className="w-full accent-blue-500"
            />
          </div>

          {/* Громкость */}
          <div className="flex items-center gap-3 mb-4 bg-zinc-800 rounded-2xl px-4 py-2.5">
            <Volume2 size={16} className="text-zinc-400 flex-shrink-0" />
            <input
              type="range"
              min="0"
              max="100"
              value={settings.volume}
              onChange={(e) => onSlider('volume', Number(e.target.value))}
              className="w-full accent-blue-500"
            />
          </div>

          {/* Уведомления */}
          <div className="text-xs text-zinc-500 px-1 mb-1.5">Уведомления</div>
          <button
            onClick={onOpenMessenger}
            className="w-full flex items-center gap-3 bg-zinc-800 rounded-2xl px-3 py-2.5 mb-3 text-left active:scale-[0.98] transition-transform"
          >
            <div className="w-9 h-9 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
              <MessageSquare size={16} className="text-white" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-sm font-semibold text-white">Сообщения</div>
              <div className="text-xs text-zinc-400 truncate">
                {hasUnread ? '@m_lebedeva_press: новое сообщение' : 'Нет новых сообщений'}
              </div>
            </div>
          </button>

          {/* Ручка для закрытия */}
          <button
            onClick={onClose}
            className="w-full flex justify-center py-1 text-zinc-500 active:opacity-60"
          >
            <ChevronUp size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
