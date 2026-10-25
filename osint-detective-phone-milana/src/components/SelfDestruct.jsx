import { useState, useEffect } from 'react';

export default function SelfDestruct({ text, onFinish, delay = 2000, speed = 60 }) {
  const [displayed, setDisplayed] = useState(text);
  const [phase, setPhase] = useState('idle'); // idle → deleting → threat → gone

  useEffect(() => {
    // Стартуем удаление через `delay` мс
    const start = setTimeout(() => setPhase('deleting'), delay);
    return () => clearTimeout(start);
  }, [delay]);

  useEffect(() => {
    if (phase !== 'deleting') return;
    if (displayed.length === 0) {
      setTimeout(() => setPhase('threat'), 400);
      return;
    }
    const t = setTimeout(() => setDisplayed((s) => s.slice(0, -1)), speed);
    return () => clearTimeout(t);
  }, [phase, displayed, speed]);

  useEffect(() => {
    if (phase !== 'threat') return;
    const t = setTimeout(() => {
      setPhase('gone');
      onFinish?.();
    }, 2500);
    return () => clearTimeout(t);
  }, [phase, onFinish]);

  if (phase === 'gone') return null;

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4 text-xs text-zinc-300 whitespace-pre-wrap leading-relaxed min-h-[100px]">
      {phase === 'idle' && <span>{displayed}</span>}

      {phase === 'deleting' && (
        <span>
          {displayed}
          <span className="inline-block w-[2px] h-[14px] bg-red-500 ml-0.5 animate-pulse align-middle" />
        </span>
      )}

      {phase === 'threat' && (
        <div className="text-red-400 font-mono text-sm animate-pulse">
          <span className="text-zinc-500">$ </span>
          ХВАТИТ КОПАТЬ
        </div>
      )}
    </div>
  );
}