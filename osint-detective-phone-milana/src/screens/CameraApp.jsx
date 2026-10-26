import { useEffect, useState } from 'react';
import { ChevronLeft, RotateCw, AlertTriangle } from 'lucide-react';

export default function CameraApp({ onBack }) {
  const [glitch, setGlitch] = useState(false);
  const [facing, setFacing] = useState('back');
  const [error, setError] = useState(false);

  useEffect(() => {
    const tick = () => {
      setGlitch(true);
      setTimeout(() => setGlitch(false), 80 + Math.random() * 120);
      setTimeout(tick, 300 + Math.random() * 500);
    };
    const t = setTimeout(tick, 200);
    return () => clearTimeout(t);
  }, []);

  useEffect(() => {
    const t = setTimeout(() => setError(true), 2200);
    return () => clearTimeout(t);
  }, [facing]);

  const switchCamera = () => {
    setFacing((f) => (f === 'back' ? 'front' : 'back'));
    setError(false);
  };

  return (
    <div className="w-full h-full flex flex-col bg-black relative overflow-hidden">

      <div className="flex items-center gap-3 px-4 py-3 h-14 border-b border-zinc-800 flex-shrink-0 z-20 bg-black/80">
        <button onClick={onBack} className="text-blue-500"><ChevronLeft size={24} /></button>
        <span className="text-sm font-semibold text-white">Камера</span>
        <span className="ml-auto text-xs text-zinc-500">
          {facing === 'back' ? 'Задняя' : 'Фронтальная'}
        </span>
      </div>

      <div className="flex-1 relative overflow-hidden">
        <div className="absolute inset-0 bg-zinc-950" />

        <div
          className="absolute inset-0"
          style={{
            background:
              'radial-gradient(circle at 20% 30%, rgba(255,0,128,0.35) 0%, transparent 30%), ' +
              'radial-gradient(circle at 75% 60%, rgba(0,255,180,0.3) 0%, transparent 25%), ' +
              'radial-gradient(circle at 50% 80%, rgba(120,0,255,0.35) 0%, transparent 35%), ' +
              'radial-gradient(circle at 85% 15%, rgba(255,200,0,0.25) 0%, transparent 20%)',
            mixBlendMode: 'screen',
          }}
        />

        <div
          className="absolute inset-0"
          style={{
            backgroundImage:
              'linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px), ' +
              'linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px)',
            backgroundSize: '6px 6px',
          }}
        />

        <div
          className="absolute inset-0"
          style={{
            background:
              'repeating-linear-gradient(0deg, rgba(0,0,0,0.4) 0px, rgba(0,0,0,0.4) 2px, transparent 2px, transparent 5px)',
            mixBlendMode: 'multiply',
          }}
        />

        {glitch && (
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              backdropFilter: 'hue-rotate(180deg) contrast(2) saturate(1.5)',
              transform: `translateX(${(Math.random() - 0.5) * 12}px)`,
              mixBlendMode: 'screen',
            }}
          />
        )}

        <div
          className="absolute"
          style={{
            top: '30%',
            left: '15%',
            width: '180px',
            height: '140px',
            clipPath:
              'polygon(20% 0%, 60% 8%, 85% 15%, 100% 40%, 92% 65%, 78% 88%, 50% 95%, 25% 90%, 8% 70%, 0% 40%, 5% 15%)',
            background:
              'radial-gradient(ellipse at 40% 50%, rgba(0,0,0,1) 0%, rgba(0,0,0,0.9) 60%, rgba(0,0,0,0) 95%)',
          }}
        />
        <div
          className="absolute"
          style={{
            top: '30%',
            left: '15%',
            width: '180px',
            height: '140px',
            clipPath:
              'polygon(20% 0%, 60% 8%, 85% 15%, 100% 40%, 92% 65%, 78% 88%, 50% 95%, 25% 90%, 8% 70%, 0% 40%, 5% 15%)',
            boxShadow: '0 0 0 2px #39ff14, 0 0 20px 4px rgba(57,255,20,0.5) inset',
            mixBlendMode: 'screen',
            opacity: 0.75,
          }}
        />

        {error && (
          <div className="absolute inset-0 flex flex-col items-center justify-center z-10 pointer-events-none">
            <div className="bg-black/80 backdrop-blur-md rounded-2xl px-6 py-4 mx-6 flex items-start gap-3 border border-red-500/40">
              <AlertTriangle size={22} className="text-red-400 flex-shrink-0 mt-0.5" />
              <div>
                <div className="text-sm font-bold text-red-300 mb-1">
                  Матрица камеры повреждена
                </div>
                <div className="text-xs text-zinc-400 leading-relaxed">
                  Не удаётся получить изображение с {facing === 'back' ? 'заднего' : 'фронтального'} модуля.<br />
                  Обратитесь в сервисный центр.
                </div>
                <div className="text-[10px] text-zinc-600 mt-2 font-mono">
                  ERR_CAM_SENSOR_0x5F
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="absolute top-4 left-4 z-10 text-[10px] text-white/40 font-mono leading-tight">
          <div>ISO 6400</div>
          <div>f/1.8</div>
          <div>1/8s</div>
        </div>
      </div>

      <div className="bg-black/90 border-t border-zinc-800 px-6 py-5 flex items-center justify-around flex-shrink-0 z-20">
        <div className="w-11 h-11 rounded-lg bg-zinc-800 border border-zinc-700" />

        <button
          disabled
          className="w-16 h-16 rounded-full border-4 border-zinc-700 flex items-center justify-center opacity-50 cursor-not-allowed"
        >
          <div className="w-12 h-12 rounded-full bg-zinc-800" />
        </button>

        <button
          onClick={switchCamera}
          className="w-11 h-11 rounded-full bg-zinc-800 flex items-center justify-center active:scale-95 transition-transform"
        >
          <RotateCw size={20} className="text-white" />
        </button>
      </div>
    </div>
  );
}