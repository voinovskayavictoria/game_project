import { useState, useEffect, useRef } from 'react';
import {
  ChevronLeft, MessageCircle, Phone, Image, Settings as SettingsIcon, Lock,
  Wifi, Bluetooth, Moon, ChevronDown, X, Battery, Sun, ArrowDownLeft, ArrowUpRight,
  Delete, User, Clock, Grid3x3,
} from 'lucide-react';
import {
  MILANA_RESUME, SECURITY_QUESTIONS, THREADS, PHONE_CALLS, GALLERY_FILES, NOTIFICATIONS,
} from '../data';
import BatteryToast from '../components/BatteryToast';
import NotesApp from './NotesApp';
import MapsApp from './MapsApp';
import CameraApp from './CameraApp';

const CODEWORD = 'orbit';

const CONTACTS = [
  { name: 'Лев 💙', avatar: '🧑🏻', color: 'bg-sky-500', phone: '+7 999 555-12-34' },
  { name: 'Маша Лебедева', avatar: '📰', color: 'bg-zinc-600', phone: '+7 999 777-88-11' },
  { name: 'Герман', avatar: '😐', color: 'bg-orange-600', phone: '+7 999 111-22-33' },
  { name: 'Мама ❤️', avatar: '👩🏻', color: 'bg-pink-500', phone: '+7 916 200-30-40' },
  { name: 'Настя', avatar: '💁🏼‍♀️', color: 'bg-fuchsia-500', phone: '+7 999 444-55-66' },
  { name: 'Саша (бывший)', avatar: '🧔', color: 'bg-zinc-700', phone: '+7 999 000-11-22' },
  { name: 'Салон «Нежность»', avatar: '💅', color: 'bg-rose-400', phone: '+7 495 100-50-50' },
  { name: 'Яндекс Еда', avatar: '🍔', color: 'bg-yellow-500', phone: '8 800 555-35-35' },
];

function ToggleRow({ Icon, label, value, onToggle }) {
  return (
    <button
      onClick={onToggle}
      className={`flex items-center justify-between w-full px-4 py-3 rounded-2xl transition-colors ${
        value ? 'bg-blue-500 text-white' : 'bg-zinc-800 text-zinc-300'
      }`}
    >
      <div className="flex items-center gap-3">
        <Icon size={18} strokeWidth={1.8} />
        <span className="text-sm">{label}</span>
      </div>
      <div className={`w-10 h-6 rounded-full flex items-center px-0.5 transition-colors ${value ? 'bg-white/30' : 'bg-zinc-700'}`}>
        <div className={`w-5 h-5 bg-white rounded-full transition-transform ${value ? 'translate-x-4' : ''}`} />
      </div>
    </button>
  );
}

// ================= PHONE APP =================
function PhoneApp({ onBack }) {
  const [tab, setTab] = useState('dial');
  const [number, setNumber] = useState('');

  const press = (d) => setNumber((n) => (n + d).slice(0, 15));
  const del = () => setNumber((n) => n.slice(0, -1));

  const DIAL = [
    ['1', ''], ['2', 'ABC'], ['3', 'DEF'],
    ['4', 'GHI'], ['5', 'JKL'], ['6', 'MNO'],
    ['7', 'PQRS'], ['8', 'TUV'], ['9', 'WXYZ'],
    ['*', ''], ['0', '+'], ['#', ''],
  ];

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex items-center gap-3 px-4 py-3 h-14 border-b border-zinc-800 flex-shrink-0">
        <button onClick={onBack} className="text-blue-500"><ChevronLeft size={24} /></button>
        <span className="text-sm font-semibold">Телефон</span>
      </div>

      <div className="flex-1 overflow-y-auto">
        {tab === 'dial' && (
          <div className="flex flex-col h-full p-4">
            <div className="flex-1 flex flex-col items-center justify-center min-h-[100px]">
              <div className="text-3xl font-light tracking-wide text-white min-h-[44px] break-all text-center">
                {number || <span className="text-zinc-600">Введите номер</span>}
              </div>
            </div>

            <div className="grid grid-cols-3 gap-3 my-4">
              {DIAL.map(([digit, sub]) => (
                <button
                  key={digit}
                  onClick={() => press(digit)}
                  className="aspect-square rounded-full bg-zinc-900 hover:bg-zinc-800 active:scale-95 transition-all flex flex-col items-center justify-center border border-zinc-800"
                >
                  <span className="text-2xl text-white font-light">{digit}</span>
                  {sub && <span className="text-[9px] text-zinc-500 tracking-widest mt-0.5">{sub}</span>}
                </button>
              ))}
            </div>

            <div className="flex items-center justify-around mt-2">
              <div className="w-14" />
              <button className="w-14 h-14 rounded-full bg-green-500 hover:bg-green-600 flex items-center justify-center active:scale-95 transition-all">
                <Phone size={24} className="text-white" />
              </button>
              <button
                onClick={del}
                className="w-14 h-14 rounded-full flex items-center justify-center text-zinc-400 hover:text-white"
              >
                {number ? <Delete size={22} /> : <div className="w-14" />}
              </button>
            </div>
          </div>
        )}

        {tab === 'recent' && (
          <div className="p-3 space-y-2">
            {PHONE_CALLS.map((call, i) => (
              <div key={i} className="flex items-center gap-3 bg-zinc-900 rounded-xl p-3 border border-zinc-800">
                {call.missed ? (
                  <ArrowDownLeft size={16} className="text-red-400 flex-shrink-0" />
                ) : call.type === 'outgoing' ? (
                  <ArrowUpRight size={16} className="text-zinc-500 flex-shrink-0" />
                ) : (
                  <ArrowDownLeft size={16} className="text-zinc-500 flex-shrink-0" />
                )}
                <div className="flex-1">
                  <div className={`text-sm font-semibold ${call.missed ? 'text-red-400' : 'text-white'}`}>{call.from}</div>
                  <div className="text-xs text-zinc-400 mt-0.5">
                    {call.missed ? 'Пропущенный звонок' : call.duration}
                  </div>
                </div>
                <span className="text-xs text-zinc-500">{call.time}</span>
              </div>
            ))}
          </div>
        )}

        {tab === 'contacts' && (
          <div className="p-3 space-y-2">
            {CONTACTS.map((c, i) => (
              <div key={i} className="flex items-center gap-3 bg-zinc-900 rounded-xl p-3 border border-zinc-800">
                <div className={`w-10 h-10 ${c.color} rounded-full flex items-center justify-center text-lg flex-shrink-0`}>
                  {c.avatar}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-semibold text-white truncate">{c.name}</div>
                  <div className="text-xs text-zinc-400 mt-0.5">{c.phone}</div>
                </div>
                <button className="w-9 h-9 rounded-full bg-green-500/10 text-green-500 flex items-center justify-center">
                  <Phone size={16} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="flex justify-around items-center bg-zinc-900/95 backdrop-blur-md border-t border-zinc-800 px-2 py-2 flex-shrink-0">
        {[
          { key: 'dial', Icon: Grid3x3, label: 'Клавиатура' },
          { key: 'recent', Icon: Clock, label: 'Недавние' },
          { key: 'contacts', Icon: User, label: 'Контакты' },
        ].map(({ key, Icon, label }) => {
          const active = tab === key;
          return (
            <button
              key={key}
              onClick={() => setTab(key)}
              className={`flex flex-col items-center gap-0.5 px-4 py-1 rounded-xl transition-colors ${
                active ? 'text-blue-500' : 'text-zinc-500'
              }`}
            >
              <Icon size={18} strokeWidth={1.8} />
              <span className="text-[9px]">{label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

// ================= ГЛАВНЫЙ КОМПОНЕНТ =================
export default function MilanaPhone({ onBack, initialScreen = 'threads' }) {
  const lockType =
    initialScreen === 'threads' ? 'codeword' :
    initialScreen === 'gallery' ? 'questions' :
    null;

  const [screen, setScreen] = useState(initialScreen);
  const [unlocked, setUnlocked] = useState(!lockType);
  const [answers, setAnswers] = useState({ 0: '', 1: '', 2: '' });
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [error, setError] = useState('');
  const [codewordInput, setCodewordInput] = useState('');

  const [activeThreadId, setActiveThreadId] = useState(null);
  const [viewingPhoto, setViewingPhoto] = useState(null);
  const [toggles, setToggles] = useState({ wifi: true, bluetooth: false, dnd: false, autoBright: true });

  const [glitch, setGlitch] = useState(false);
  const [batteryLevel, setBatteryLevel] = useState(0);
  const [showBatteryToast, setShowBatteryToast] = useState(false);
  const [germanThreat, setGermanThreat] = useState(false);

  useEffect(() => {
    if (!unlocked) return;
    let timer;
    const trigger = () => {
      setGlitch(true);
      setTimeout(() => setGlitch(false), 220);
      timer = setTimeout(trigger, 30000 + Math.random() * 10000);
    };
    timer = setTimeout(trigger, 32000);
    return () => clearTimeout(timer);
  }, [unlocked]);

  useEffect(() => {
    if (screen !== 'gallery' || germanThreat) return;
    const t = setTimeout(() => setGermanThreat(true), 15000);
    return () => clearTimeout(t);
  }, [screen, germanThreat]);

  const checkAnswers = () => {
    const correct = answers[currentQuestion]?.toLowerCase().trim() === SECURITY_QUESTIONS[currentQuestion].a;
    if (correct) {
      if (currentQuestion < 2) {
        setCurrentQuestion(currentQuestion + 1);
        setError('');
      } else {
        setUnlocked(true);
      }
    } else {
      setError('Неправильно. Попробуй снова.');
      setAnswers({ ...answers, [currentQuestion]: '' });
    }
  };

  const checkCodeword = () => {
    if (codewordInput.trim().toLowerCase() === CODEWORD) {
      setUnlocked(true);
      setError('');
    } else {
      setError('Неверное кодовое слово.');
      setCodewordInput('');
    }
  };

  const handleToggle = (key) => setToggles((prev) => ({ ...prev, [key]: !prev[key] }));

  const openThread = (id) => {
    setActiveThreadId(id);
    setScreen('thread');
  };

  // ---------- ЭКРАН БЛОКИРОВКИ ----------
  if (!unlocked) {
    return (
      <div className="w-full h-full bg-gradient-to-b from-zinc-900 to-zinc-950 text-white flex flex-col items-center justify-center p-4 relative">
        <button onClick={onBack} className="absolute top-4 left-4 text-zinc-500 hover:text-white z-10">
          <ChevronLeft size={24} />
        </button>

        <div className="text-center w-full max-w-sm relative">
          <Lock size={64} className="mx-auto mb-4 text-yellow-500" />

          {lockType === 'codeword' ? (
            <>
              <h1 className="text-2xl font-bold mb-2">Переписки защищены</h1>
              <p className="text-zinc-400 text-sm mb-6">Введите кодовое слово, чтобы открыть сообщения</p>
              <div className="bg-zinc-800 rounded-2xl p-6 mb-4">
                <input
                  type="text"
                  placeholder="Кодовое слово..."
                  value={codewordInput}
                  onChange={(e) => setCodewordInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && checkCodeword()}
                  className="w-full px-4 py-3 bg-zinc-700 border border-zinc-600 rounded-lg text-white text-center mb-4 focus:outline-none focus:border-blue-500"
                  autoFocus
                />
                {error && <p className="text-red-400 text-xs mb-4">{error}</p>}
                <button
                  onClick={checkCodeword}
                  className="w-full py-2 bg-blue-500 hover:bg-blue-600 rounded-lg font-semibold transition-colors"
                >
                  Разблокировать
                </button>
              </div>
            </>
          ) : (
            <>
              <h1 className="text-2xl font-bold mb-2">Галерея защищена</h1>
              <p className="text-zinc-400 text-sm mb-6">Ответь на вопросы из резюме, чтобы открыть галерею</p>
              <div className="bg-zinc-800 rounded-2xl p-6 mb-4">
                <p className="text-sm text-zinc-300 mb-4">{currentQuestion + 1}/3</p>
                <div className="w-full bg-zinc-700 rounded-full h-1 mb-6">
                  <div
                    className="bg-blue-500 h-1 rounded-full transition-all"
                    style={{ width: `${((currentQuestion + 1) / 3) * 100}%` }}
                  ></div>
                </div>
                <p className="text-sm font-semibold mb-4">{SECURITY_QUESTIONS[currentQuestion].q}</p>
                <input
                  type="text"
                  placeholder="Ответ..."
                  value={answers[currentQuestion] || ''}
                  onChange={(e) => setAnswers({ ...answers, [currentQuestion]: e.target.value })}
                  onKeyPress={(e) => e.key === 'Enter' && checkAnswers()}
                  className="w-full px-4 py-2 bg-zinc-700 border border-zinc-600 rounded-lg text-white mb-4 focus:outline-none focus:border-blue-500"
                  autoFocus
                />
                {error && <p className="text-red-400 text-xs mb-4">{error}</p>}
                <button
                  onClick={checkAnswers}
                  className="w-full py-2 bg-blue-500 hover:bg-blue-600 rounded-lg font-semibold transition-colors"
                >
                  Далее
                </button>
              </div>
              <p className="text-xs text-zinc-500">Подсказка: смотри резюме</p>
            </>
          )}
        </div>
      </div>
    );
  }

  const activeThread = THREADS.find((t) => t.id === activeThreadId);

  // ---------- ОСНОВНОЙ ИНТЕРФЕЙС ----------
  return (
    <div className="relative w-full h-full bg-zinc-950 text-white font-sans flex flex-col overflow-hidden select-none pt-8">

      {glitch && (
        <div
          className="absolute inset-0 z-[105] pointer-events-none"
          style={{
            backdropFilter: 'hue-rotate(180deg) contrast(1.4)',
            transform: 'translateX(3px)',
            mixBlendMode: 'screen',
            background:
              'repeating-linear-gradient(0deg, rgba(255,255,255,0.06) 0px, rgba(0,0,0,0.06) 2px, transparent 2px, transparent 4px)',
          }}
        />
      )}

      {showBatteryToast && (
        <BatteryToast level={batteryLevel} onDismiss={() => {
          setShowBatteryToast(false);
          setBatteryLevel((l) => Math.min(l + 1, 2));
        }} />
      )}

      {germanThreat && (
        <div className="absolute top-12 left-3 right-3 z-[110]">
          <div className="bg-orange-600/95 backdrop-blur-md rounded-2xl px-4 py-3 flex items-start gap-3 shadow-2xl border border-orange-400">
            <div className="w-4 h-4 rounded-full bg-white flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <div className="flex justify-between items-center mb-1">
                <span className="text-xs font-bold text-white">Герман</span>
                <span className="text-[10px] text-orange-100">сейчас</span>
              </div>
              <div className="text-xs text-white leading-relaxed">
                «Я знаю, что телефон у тебя. Не лезь в это.»
              </div>
            </div>
            <button onClick={() => setGermanThreat(false)} className="text-white/70 hover:text-white">
              <X size={16} />
            </button>
          </div>
        </div>
      )}

      <div className="flex-1 overflow-hidden relative">

        {screen === 'threads' && (
          <div className="w-full h-full flex flex-col">
            <div className="flex items-center gap-3 px-4 py-3 h-14 border-b border-zinc-800 flex-shrink-0">
              <button onClick={onBack} className="text-blue-500"><ChevronLeft size={24} /></button>
              <span className="text-sm font-semibold">Сообщения</span>
            </div>
            <div className="flex-1 overflow-y-auto">
              {THREADS.map((t) => {
                const last = t.messages[t.messages.length - 1];
                return (
                  <button
                    key={t.id}
                    onClick={() => openThread(t.id)}
                    className="w-full flex items-center gap-3 px-4 py-3 border-b border-zinc-900 hover:bg-zinc-900 text-left"
                  >
                    <div className={`w-11 h-11 ${t.color} rounded-full flex items-center justify-center text-lg flex-shrink-0`}>{t.avatar}</div>
                    <div className="flex-1 min-w-0">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-semibold text-white">{t.name}</span>
                        <span className="text-[10px] text-zinc-500">{last.time}</span>
                      </div>
                      <div className="text-xs text-zinc-400 truncate">{last.text}</div>
                    </div>
                    {t.unread && <div className="w-2.5 h-2.5 bg-blue-500 rounded-full flex-shrink-0"></div>}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {screen === 'thread' && activeThread && (
          <div className="w-full h-full flex flex-col">
            <div className="flex items-center gap-3 px-4 py-3 h-14 border-b border-zinc-800 flex-shrink-0">
              <button onClick={() => setScreen('threads')} className="text-blue-500"><ChevronLeft size={24} /></button>
              <div className={`w-8 h-8 ${activeThread.color} rounded-full flex items-center justify-center text-sm`}>{activeThread.avatar}</div>
              <span className="text-sm font-semibold">{activeThread.name}</span>
            </div>
            <div className="flex-1 overflow-y-auto p-3 flex flex-col gap-1.5">
              {activeThread.messages.map((m, i) => (
                <div key={i} className={`flex ${m.who === 'me' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[75%] rounded-2xl px-3.5 py-2 text-sm leading-relaxed ${
                    m.who === 'me' ? 'bg-blue-500 text-white' : 'bg-zinc-800 text-white'
                  }`}>
                    {m.text}
                    <div className={`text-[9px] mt-1 ${m.who === 'me' ? 'text-blue-100/70' : 'text-zinc-500'}`}>{m.time}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {screen === 'phone' && <PhoneApp onBack={onBack} />}

        {screen === 'gallery' && (
          <div className="w-full h-full flex flex-col">
            <div className="flex items-center gap-3 px-4 py-3 h-14 border-b border-zinc-800 flex-shrink-0">
              <button onClick={onBack} className="text-blue-500"><ChevronLeft size={24} /></button>
              <span className="text-sm font-semibold">Галерея</span>
            </div>
            
            <div className="flex-1 overflow-y-auto p-3 grid grid-cols-2 gap-2 auto-rows-max">
              {GALLERY_FILES.map((file) => (
                <button
                  key={file.id}
                  onClick={() => file.type !== 'deleted' && setViewingPhoto(file)}
                  className={`relative w-full aspect-square rounded-xl overflow-hidden flex items-center justify-center bg-zinc-900 border border-zinc-800 ${
                    file.type === 'deleted' ? 'opacity-40 cursor-default grayscale' : 'hover:opacity-80 transition-opacity'
                  }`}
                >
                  <img
                    src={file.url}
                    alt="" 
                    loading="lazy"
                    decoding="async"
                    className="w-full h-full object-cover z-10"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                  
                  {file.type === 'screenshot' && (
                    <div className="absolute bottom-0 left-0 right-0 bg-blue-600/90 text-[10px] text-white p-1 z-20 text-center uppercase tracking-wider">
                      Скриншот
                    </div>
                  )}
                </button>
              ))}
            </div>
          
          </div>
        )}

        {screen === 'settings' && (
          <div className="w-full h-full flex flex-col">
            <div className="flex items-center gap-3 px-4 py-3 h-14 border-b border-zinc-800 flex-shrink-0">
              <button onClick={onBack} className="text-blue-500"><ChevronLeft size={24} /></button>
              <span className="text-sm font-semibold">Настройки</span>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-2">
              <ToggleRow Icon={Wifi} label="Wi-Fi" value={toggles.wifi} onToggle={() => handleToggle('wifi')} />
              <ToggleRow Icon={Bluetooth} label="Bluetooth" value={toggles.bluetooth} onToggle={() => handleToggle('bluetooth')} />
              <ToggleRow Icon={Moon} label="Не беспокоить" value={toggles.dnd} onToggle={() => handleToggle('dnd')} />
              <ToggleRow Icon={Sun} label="Автояркость" value={toggles.autoBright} onToggle={() => handleToggle('autoBright')} />

              <div className="text-xs text-zinc-500 px-1 pt-4 pb-1">Об устройстве</div>
              <div className="bg-zinc-900 rounded-2xl p-4 border border-zinc-800 space-y-2 text-sm">
                <div className="flex justify-between"><span className="text-zinc-500">Владелец</span><span>{MILANA_RESUME.name}</span></div>
                <div className="flex justify-between"><span className="text-zinc-500">Почта</span><span className="text-xs">{MILANA_RESUME.email}</span></div>
                <div className="flex justify-between"><span className="text-zinc-500">Компания</span><span>{MILANA_RESUME.company}</span></div>
                <div className="flex justify-between"><span className="text-zinc-500">Модель</span><span>Galaxy S23</span></div>
                <div className="flex justify-between items-center"><span className="text-zinc-500">Батарея</span><span className="flex items-center gap-1"><Battery size={14}/> 12%</span></div>
              </div>
            </div>
          </div>
        )}

        {screen === 'notes' && <NotesApp onBack={onBack} />}
        {screen === 'maps' && <MapsApp onBack={onBack} />}
        {screen === 'camera' && <CameraApp onBack={onBack} />}
      </div>

      {viewingPhoto && (
        <div className="absolute inset-0 z-[70] bg-black/95 flex flex-col items-center justify-center p-4 backdrop-blur-sm" onClick={() => setViewingPhoto(null)}>
          <button className="absolute top-4 right-4 text-white/70 hover:text-white" onClick={() => setViewingPhoto(null)}><X size={24} /></button>
          
          <div className="w-full max-w-sm rounded-2xl overflow-hidden flex items-center justify-center">
            <img 
              src={viewingPhoto.url} 
              alt="" 
              className="w-full max-h-[70vh] object-contain"
            />
          </div>
        </div>
      )}
    </div>
  );
}