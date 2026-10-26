export default function BrokenScreen() {
  return (
    <div className="absolute inset-0 pointer-events-none z-[200]">

      {/* 1. Текстура разбитого стекла — PNG с тайлингом по вертикали */}
      <div
        className="absolute inset-0 mix-blend-screen opacity-55"
        style={{
          backgroundImage: "url('/crack-texture.png')",
          backgroundSize: '380px 534px',
          backgroundRepeat: 'repeat-y',
          backgroundPosition: 'top center',
        }}
      />

      {/* 2. CSS-фолбэк трещин — на случай, если PNG не загрузится */}
      <svg
        viewBox="0 0 400 800"
        preserveAspectRatio="none"
        className="absolute inset-0 w-full h-full opacity-60"
      >
        <defs>
          <linearGradient id="crack" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="rgba(255,255,255,0)" />
            <stop offset="50%" stopColor="rgba(255,255,255,0.7)" />
            <stop offset="100%" stopColor="rgba(255,255,255,0)" />
          </linearGradient>
        </defs>
        <g stroke="url(#crack)" strokeWidth="1.4" fill="none">
          <path d="M 20 30 L 120 180 L 180 220 L 240 290 L 300 340 L 360 380" />
          <path d="M 120 180 L 90 260 L 130 340 L 80 420" />
          <path d="M 180 220 L 220 200 L 280 240 L 320 300" />
          <path d="M 240 290 L 260 400 L 320 500 L 340 620" />
          <path d="M 130 340 L 80 420 L 60 520 L 90 720" />
        </g>
        <g stroke="rgba(255,255,255,0.35)" strokeWidth="0.7" fill="none">
          <path d="M 140 200 L 160 150 L 200 100" />
          <path d="M 200 260 L 240 320 L 300 380" />
          <path d="M 100 300 L 60 340 L 30 400" />
          <path d="M 280 420 L 340 440 L 380 500" />
          <path d="M 70 600 L 120 640 L 180 680" />
        </g>
      </svg>

      {/* 3. Мёртвая матрица сверху-справа — рваная клякса с зелёной каймой */}
      <div
        className="absolute"
        style={{
          top: '14%',
          right: '-10px',
          width: '130px',
          height: '130px',
          clipPath:
            'polygon(50% 0%, 70% 10%, 85% 5%, 95% 25%, 100% 45%, 90% 60%, 95% 80%, 75% 90%, 55% 95%, 35% 88%, 15% 95%, 5% 75%, 0% 55%, 8% 35%, 15% 15%, 30% 8%)',
          background:
            'radial-gradient(circle at 40% 40%, rgba(0,0,0,1) 0%, rgba(0,0,0,0.95) 50%, rgba(0,0,0,0.7) 70%, rgba(0,0,0,0) 95%)',
        }}
      />
      <div
        className="absolute"
        style={{
          top: '14%',
          right: '-10px',
          width: '130px',
          height: '130px',
          clipPath:
            'polygon(50% 0%, 70% 10%, 85% 5%, 95% 25%, 100% 45%, 90% 60%, 95% 80%, 75% 90%, 55% 95%, 35% 88%, 15% 95%, 5% 75%, 0% 55%, 8% 35%, 15% 15%, 30% 8%)',
          boxShadow: '0 0 0 2px #39ff14, 0 0 12px 2px rgba(57,255,20,0.6) inset',
          mixBlendMode: 'screen',
          opacity: 0.85,
        }}
      />

      {/* 4. Мёртвая матрица снизу-слева — фиолетовая кайма */}
      <div
        className="absolute"
        style={{
          bottom: '20%',
          left: '-20px',
          width: '100px',
          height: '100px',
          clipPath:
            'polygon(30% 0%, 60% 5%, 80% 20%, 95% 45%, 90% 70%, 70% 90%, 40% 95%, 15% 85%, 5% 60%, 10% 30%, 20% 10%)',
          background:
            'radial-gradient(circle at 60% 50%, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.8) 60%, rgba(0,0,0,0) 95%)',
        }}
      />
      <div
        className="absolute"
        style={{
          bottom: '20%',
          left: '-20px',
          width: '100px',
          height: '100px',
          clipPath:
            'polygon(30% 0%, 60% 5%, 80% 20%, 95% 45%, 90% 70%, 70% 90%, 40% 95%, 15% 85%, 5% 60%, 10% 30%, 20% 10%)',
          boxShadow: '0 0 0 1.5px #b026ff, 0 0 10px 2px rgba(176,38,255,0.5) inset',
          mixBlendMode: 'screen',
          opacity: 0.8,
        }}
      />

      {/* 5. Отпечатки и пыль — самый верхний слой */}
      <div
        className="absolute inset-0"
        style={{
          backgroundImage:
            "radial-gradient(circle at 25% 40%, rgba(255,255,255,0.06) 0%, transparent 3%), radial-gradient(circle at 70% 65%, rgba(255,255,255,0.05) 0%, transparent 4%), radial-gradient(circle at 45% 85%, rgba(255,255,255,0.04) 0%, transparent 3%), radial-gradient(circle at 80% 20%, rgba(255,255,255,0.05) 0%, transparent 2%)",
          opacity: 0.8,
          mixBlendMode: 'overlay',
        }}
      />

      {/* 6. Тонкая пиксельная сетка поверх всего */}
      <div
        className="absolute inset-0"
        style={{
          background:
            'repeating-linear-gradient(0deg, rgba(255,255,255,0.015) 0px, rgba(255,255,255,0.015) 1px, transparent 1px, transparent 3px)',
          mixBlendMode: 'overlay',
          opacity: 0.6,
        }}
      />
    </div>
  );
}