import { useEffect, useState } from 'react';
import { Battery } from 'lucide-react';

const MESSAGES = [
  'Батарея разряжена (9%). Включить режим энергосбережения?',
  'Низкий заряд (6%). Некоторые функции могут быть недоступны.',
  'Критический уровень (3%). Телефон скоро отключится.',
];

export default function BatteryToast({ level, onDismiss }) {
  const [visible, setVisible] = useState(true);
  const msg = MESSAGES[Math.min(level, MESSAGES.length - 1)];

  useEffect(() => {
    const t = setTimeout(() => {
      setVisible(false);
      onDismiss?.();
    }, 4000);
    return () => clearTimeout(t);
  }, [onDismiss]);

  if (!visible) return null;

  return (
    <div className="absolute top-12 left-3 right-3 z-[95] animate-[slideDown_0.3s_ease-out]">
      <div className="bg-zinc-800/95 backdrop-blur-md border border-zinc-700 rounded-2xl px-4 py-3 flex items-start gap-3 shadow-2xl">
        <Battery size={18} className="text-red-400 flex-shrink-0 mt-0.5" />
        <div className="flex-1 text-xs text-zinc-200 leading-relaxed">{msg}</div>
      </div>
      <style>{`
        @keyframes slideDown {
          from { transform: translateY(-20px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }
      `}</style>
    </div>
  );
}