import { useState } from 'react';
import { ChevronLeft, RotateCw, Lock } from 'lucide-react';

const TABS = [
  { id: 'home', label: 'Главная' },
  { id: 'about', label: 'О нас' },
  { id: 'archive', label: 'Архив' },
  { id: 'contacts', label: 'Контакты' },
];

export default function BrowserApp({ onBack }) {
  const [tab, setTab] = useState('home');

  return (
    <div className="relative w-full h-full bg-zinc-950 text-white font-sans flex flex-col overflow-hidden">
      {/* Шапка браузера */}
      <div className="flex items-center gap-2 px-3 py-2.5 h-14 flex-shrink-0 border-b border-zinc-800">
        <button
          onClick={onBack}
          className="w-9 h-9 rounded-full hover:bg-zinc-800 flex items-center justify-center text-blue-500 transition-colors flex-shrink-0"
        >
          <ChevronLeft size={22} />
        </button>
        <div className="flex-1 flex items-center gap-2 bg-zinc-900 border border-zinc-800 rounded-full px-3 py-1.5 text-xs text-zinc-400">
          <Lock size={11} className="text-green-500 flex-shrink-0" />
          <span className="truncate">primesystems.io</span>
        </div>
        <button className="w-9 h-9 rounded-full hover:bg-zinc-800 flex items-center justify-center text-zinc-400 flex-shrink-0">
          <RotateCw size={16} />
        </button>
      </div>

      {/* Вкладки сайта */}
      <div className="flex gap-1 px-3 py-2 border-b border-zinc-900 flex-shrink-0 overflow-x-auto">
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`px-3 py-1.5 rounded-full text-xs whitespace-nowrap transition-colors ${
              tab === t.id ? 'bg-blue-500 text-white' : 'bg-zinc-900 text-zinc-400'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Контент страницы */}
      <div className="flex-1 overflow-y-auto px-4 py-4 text-sm leading-relaxed text-zinc-300">
        {tab === 'home' && (
          <div>
            <div className="text-lg font-semibold text-white mb-2">PRIME SYSTEMS</div>
            <div className="text-zinc-400 mb-4">Разработка защищённых программных решений для бизнеса.</div>
            <div className="bg-zinc-900 rounded-2xl p-3 mb-3 border border-zinc-800">
              <div className="text-white font-medium mb-1">Наши направления</div>
              <div className="text-xs text-zinc-400">Корпоративные системы связи · базы данных · инфраструктурные решения под заказ.</div>
            </div>
            <div className="text-xs text-zinc-500">© PRIME SYSTEMS, 2015–2020. Сайт не обновлялся с 2020 года.</div>
          </div>
        )}

        {tab === 'about' && (
          <div>
            <div className="text-lg font-semibold text-white mb-2">О компании</div>
            <div className="mb-3 text-zinc-400">
              Небольшая команда разработчиков, специализирующаяся на закрытых системах связи
              и хранения данных для юридического и финансового секторов.
            </div>
            <div className="bg-zinc-900 rounded-2xl p-3 border border-zinc-800">
              <div className="text-white font-medium mb-1">Команда</div>
              <div className="text-xs text-zinc-400">Основатель — Соколов. Ключевые разработчики — Лев, Герман.</div>
            </div>
          </div>
        )}

        {tab === 'archive' && (
          <div>
            <div className="text-lg font-semibold text-white mb-2">Архив проектов</div>
            <div className="bg-zinc-900 rounded-2xl p-3 border border-zinc-800 mb-3">
              <div className="text-xs text-zinc-500 mb-1">Опубликовано: 2020</div>
              <div className="text-white text-sm mb-1">Обновление по проекту C-17</div>
              <div className="text-xs text-zinc-400 leading-relaxed">
                Инфраструктура C-17 передана на обслуживание в компанию ORBIT DATA в связи
                с ужесточением требований к защите персональных данных и адвокатской тайны.
                Дальнейшая поддержка и эксплуатация осуществляются исключительно силами
                оператора ORBIT DATA. PRIME SYSTEMS более не участвует в сопровождении проекта.
              </div>
            </div>
            <div className="text-xs text-zinc-600">Других записей в архиве не найдено.</div>
          </div>
        )}

        {tab === 'contacts' && (
          <div>
            <div className="text-lg font-semibold text-white mb-2">Контакты</div>
            <div className="text-xs text-zinc-400 mb-1">Почта: info@primesystems.io</div>
            <div className="text-xs text-zinc-400">Форма обратной связи временно недоступна.</div>
          </div>
        )}
      </div>
    </div>
  );
}
