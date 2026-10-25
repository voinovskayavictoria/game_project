// src/components/GlobalShade.jsx
import { useState } from 'react';
import {
  Wifi, Bluetooth, Moon, Sun, ChevronDown, Flashlight, Plane,
  BellOff, RotateCcw, Volume2,
} from 'lucide-react';
import { NOTIFICATIONS } from '../data';

const TOGGLES = [
  { key: 'wifi', Icon: Wifi, label: 'Wi-Fi' },
  { key: 'bluetooth', Icon: Bluetooth, label: 'Bluetooth' },
  { key: 'flashlight', Icon: Flashlight, label: 'Фонарик' },
  { key: 'airplane', Icon: Plane, label: 'Полёт' },
  { key: 'dnd', Icon: BellOff, label: 'Не беспокоить' },
  { key: 'autoRotate', Icon: RotateCcw, label: 'Автоповорот' },
];

export default function GlobalShade({ onOpenThread }) {
  const [open, setOpen] = useState(false);
  const [toggles, setToggles] = useState({
    wifi: true, bluetooth: false, flashlight: false,
    airplane: false, dnd: false, autoRotate: true,
  });
  const [brightness, setBrightness] = useState(70);
  const [volume, setVolume] = useState(60);

  const time = new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });

  const handleToggle = (key) => setToggles((p) => ({ ...p, [key]: !p[key] }));

  return (
    <>
      {/* Статус-бар — висит поверх контента, клик открывает шторку */}
      <div
        onClick={() => setOpen(true)}
        className="absolute top-0 left-0 right-0 z-[85] flex justify-between items-center px-4 pt-3 pb-2 text-xs font-medium text-zinc-300 cursor-pointer active:bg-white/5"
      >
        <span className="drop-shadow">{time}</span>
        <ChevronDown size={13} className="text-zinc-400" />
        <div className="flex gap-1 items-center">
          <span>📶</span>
          <div className="flex items-center gap-1 text-white">
            <svg width="18" height="11" viewBox="0 0 18 11">
              <rect x="0.5" y="0.5" width="14" height="10" rx="2" stroke="white" strokeWidth="0.8" fill="none" />
              <rect x="2" y="2" width="10" height="7" rx="1" fill="white" />
              <rect x="15.5" y="3.5" width="1.5" height="4" rx="0.5" fill="white" />
            </svg>
            <span className="text-[10px]">12</span>
          </div>
        </div>
      </div>

      {/* Шторка */}
      <div className={`absolute inset-0 z-[90] transition-opacity duration-300 ${open ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}>
        <div className="absolute inset-0 bg-black/50" onClick={() => setOpen(false)} />
        <div className={`absolute top-0 left-0 right-0 bg-zinc-900/95 backdrop-blur-md rounded-b-[28px] shadow-2xl transition-transform duration-300 ${open ? 'translate-y-0' : '-translate-y-full'}`}>
          <div className="pt-8 pb-3 px-4">
            <div className="grid grid-cols-3 gap-3 mb-4">
              {TOGGLES.map(({ key, Icon, label }) => {
                const active = toggles[key];
                return (
                  <button
                    key={key}
                    onClick={() => handleToggle(key)}
                    className={`flex flex-col items-center justify-center gap-1.5 py-3 rounded-2xl transition-colors ${active ? 'bg-blue-500 text-white' : 'bg-zinc-800 text-zinc-300'}`}
                  >
                    <Icon size={20} strokeWidth={1.8} />
                    <span className="text-[10px] leading-none text-center px-1">{label}</span>
                  </button>
                );
              })}
            </div>

            <div className="flex items-center gap-3 mb-3 bg-zinc-800 rounded-2xl px-4 py-2.5">
              <Sun size={16} className="text-zinc-400" />
              <input type="range" min="0" max="100" value={brightness}
                onChange={(e) => setBrightness(Number(e.target.value))}
                className="w-full accent-blue-500" />
            </div>

            <div className="flex items-center gap-3 mb-4 bg-zinc-800 rounded-2xl px-4 py-2.5">
              <Volume2 size={16} className="text-zinc-400" />
              <input type="range" min="0" max="100" value={volume}
                onChange={(e) => setVolume(Number(e.target.value))}
                className="w-full accent-blue-500" />
            </div>

            <div className="text-xs text-zinc-500 px-1 mb-1.5">Уведомления</div>
            <div className="space-y-1.5 max-h-72 overflow-y-auto pb-2">
              {NOTIFICATIONS.map((n, i) => (
                <button
                  key={i}
                  onClick={() => {
                    if (n.threadId && onOpenThread) onOpenThread(n.threadId);
                    setOpen(false);
                  }}
                  className="w-full flex items-center gap-3 bg-zinc-800 rounded-2xl px-3 py-2.5 text-left active:scale-[0.98]"
                >
                  <div className="w-9 h-9 bg-zinc-700 rounded-full flex items-center justify-center text-base flex-shrink-0">{n.icon}</div>
                  <div className="flex-1 min-w-0">
                    <div className="flex justify-between">
                      <span className="text-xs font-semibold text-white">{n.app}</span>
                      <span className="text-[10px] text-zinc-500">{n.time}</span>
                    </div>
                    <div className="text-xs text-zinc-400 truncate">{n.text}</div>
                  </div>
                </button>
              ))}
            </div>

            <button onClick={() => setOpen(false)} className="w-full flex justify-center py-2 text-zinc-500">
              <ChevronDown size={20} className="rotate-180" />
            </button>
          </div>
        </div>
      </div>
    </>
  );
}