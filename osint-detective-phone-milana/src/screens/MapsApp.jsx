import { ChevronLeft, MapPin } from 'lucide-react';

export default function MapsApp({ onBack }) {
  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex items-center gap-3 px-4 py-3 h-14 border-b border-zinc-800 flex-shrink-0">
        <button onClick={onBack} className="text-blue-500"><ChevronLeft size={24} /></button>
        <span className="text-sm font-semibold">Локатор</span>
      </div>

      {/* Фейковая карта */}
      <div className="flex-1 relative bg-zinc-900 overflow-hidden">
        <svg viewBox="0 0 400 700" className="w-full h-full" preserveAspectRatio="none">
          {/* Реки, дороги */}
          <path d="M 0 200 Q 150 260 400 180" stroke="#1e3a5f" strokeWidth="14" fill="none" />
          <path d="M 200 0 L 220 700" stroke="#2a2a2a" strokeWidth="8" />
          <path d="M 0 400 L 400 450" stroke="#2a2a2a" strokeWidth="6" />
          <path d="M 100 0 L 80 700" stroke="#2a2a2a" strokeWidth="4" />
          <path d="M 300 0 L 340 700" stroke="#2a2a2a" strokeWidth="4" />

          {/* Кварталы */}
          <g fill="#1a1a1c">
            <rect x="30" y="50" width="60" height="80" rx="4" />
            <rect x="120" y="80" width="60" height="90" rx="4" />
            <rect x="240" y="60" width="50" height="100" rx="4" />
            <rect x="30" y="220" width="70" height="90" rx="4" />
            <rect x="240" y="260" width="80" height="110" rx="4" />
            <rect x="60" y="500" width="90" height="120" rx="4" />
            <rect x="240" y="480" width="100" height="130" rx="4" />
          </g>

          {/* Промзона (место, где нашли телефон) */}
          <rect x="150" y="470" width="70" height="150" fill="#3a1c1c" rx="4" />
          <text x="185" y="555" fill="#a05050" fontSize="10" textAnchor="middle">ПРОМЗОНА</text>
        </svg>

        {/* Красная мигающая точка */}
        <div className="absolute" style={{ top: '64%', left: '48%' }}>
          <span className="relative flex h-4 w-4">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-4 w-4 bg-red-500 border-2 border-white"></span>
          </span>
        </div>

        {/* Карточка с адресом */}
        <div className="absolute bottom-4 left-3 right-3 bg-zinc-900/95 backdrop-blur-md rounded-2xl p-4 border border-zinc-800">
          <div className="flex items-start gap-3">
            <div className="w-9 h-9 bg-red-500 rounded-full flex items-center justify-center flex-shrink-0">
              <MapPin size={18} className="text-white" />
            </div>
            <div className="flex-1">
              <div className="text-sm font-semibold text-white">Последняя геопозиция</div>
              <div className="text-xs text-zinc-400 mt-1">
                Зафиксирована 24.05.2025 в 03:47<br />
                Промзона, ул. Заводская, 17, корпус 4
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}