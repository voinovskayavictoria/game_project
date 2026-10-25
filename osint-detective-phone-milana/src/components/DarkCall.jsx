import { useState, useEffect } from 'react';
import { Phone, PhoneOff, Mic } from 'lucide-react';

export default function DarkCall({ onEnd }) {
  const [stage, setStage] = useState('ringing'); // ringing → connected → glitch → end
  const [timer, setTimer] = useState(0);

  useEffect(() => {
    if (stage === 'connected') {
      const t = setInterval(() => setTimer((s) => s + 1), 1000);
      return () => clearInterval(t);
    }
  }, [stage]);

  const accept = () => {
    setStage('connected');
    setTimeout(() => setStage('glitch'), 3500);
    setTimeout(() => onEnd(), 4200);
  };

  const decline = () => {
    // Сброс НЕ работает — звонок продолжается (это фича)
    setStage('ringing');
  };

  const fmt = (s) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;

  return (
    <div className="absolute inset-0 z-[150] flex flex-col overflow-hidden">
      <div
        className={`absolute inset-0 ${
          stage === 'glitch' ? 'bg-red-900' : 'bg-gradient-to-b from-zinc-900 to-black'
        } transition-colors duration-150`}
      />

      {stage === 'glitch' && (
        <div
          className="absolute inset-0 z-10 pointer-events-none"
          style={{
            backdropFilter: 'hue-rotate(180deg) contrast(2)',
            background:
              'repeating-linear-gradient(0deg, rgba(255,0,0,0.4) 0px, rgba(0,0,0,0.4) 3px, transparent 3px, transparent 6px)',
          }}
        />
      )}

      <div className="relative z-20 flex-1 flex flex-col items-center justify-between p-8 text-white">
        <div className="text-center mt-12">
          <div className="text-xs text-red-400 tracking-widest mb-2">
            {stage === 'ringing' && '▲ ВХОДЯЩИЙ'}
            {stage === 'connected' && '● ЗАЩИЩЁННЫЙ КАНАЛ'}
            {stage === 'glitch' && '⚠ ОШИБКА КАНАЛА'}
          </div>
          <div className={`text-3xl font-mono tracking-wider mb-2 ${stage === 'glitch' ? 'text-red-300' : ''}`}>
            NODE_OD17
          </div>
          <div className="text-xs text-zinc-500 font-mono">
            IP: <span className="text-zinc-400">45.13.███.██</span>
          </div>

          {stage === 'ringing' && (
            <div className="mt-4 text-sm text-zinc-400 animate-pulse">Входящий вызов…</div>
          )}

          {stage === 'connected' && (
            <div className="mt-4 text-sm text-zinc-400 font-mono">{fmt(timer)}</div>
          )}
        </div>

        {stage === 'connected' && (
          <div className="text-center px-4">
            <div className="flex justify-center gap-1 mb-4">
              {[...Array(6)].map((_, i) => (
                <div
                  key={i}
                  className="w-1 bg-red-500 rounded-full animate-pulse"
                  style={{ height: `${12 + Math.random() * 24}px`, animationDelay: `${i * 0.1}s` }}
                />
              ))}
            </div>
            <div className="text-sm text-zinc-300 italic leading-relaxed">
              «Соединение установлено.<br />
              Координаты зафиксированы.<br />
              Не двигайся.»
            </div>
          </div>
        )}

        {stage === 'glitch' && (
          <div className="text-center">
            <div className="text-4xl font-bold text-red-400 animate-pulse">[!]</div>
            <div className="text-xs text-red-300 mt-2 font-mono">SIGNAL LOST</div>
          </div>
        )}

        {stage === 'ringing' && (
          <div className="flex justify-around w-full max-w-xs mb-12">
            <button
              onClick={decline}
              className="w-16 h-16 rounded-full bg-red-500 flex items-center justify-center hover:bg-red-600 active:scale-95 transition-all"
            >
              <PhoneOff size={26} className="text-white" />
            </button>
            <button
              onClick={accept}
              className="w-16 h-16 rounded-full bg-green-500 flex items-center justify-center hover:bg-green-600 active:scale-95 transition-all animate-bounce"
            >
              <Phone size={26} className="text-white" />
            </button>
          </div>
        )}

        {stage === 'connected' && (
          <div className="mb-12 flex flex-col items-center gap-4">
            <div className="text-xs text-zinc-500 flex items-center gap-2">
              <Mic size={12} /> микрофон активен
            </div>
            <button
              onClick={() => setStage('glitch')}
              className="w-16 h-16 rounded-full bg-red-500 flex items-center justify-center hover:bg-red-600 active:scale-95 transition-all"
            >
              <PhoneOff size={26} className="text-white" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}