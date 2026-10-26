import { ChevronLeft } from 'lucide-react';

const CONTENT = {
  phone: { title: 'Телефон', text: 'Журнал звонков пуст.' },
  gallery: { title: 'Галерея', text: 'Фотографий нет.' },
  mail: { title: 'Почта', text: 'Входящих писем нет.' },
  files: { title: 'Мои файлы', text: 'Папка пуста.' },
  settings: { title: 'Настройки', text: 'Здесь пока нечего настраивать.' },
  camera: { title: 'Камера', text: 'Камера недоступна на этом устройстве.' },
};

export default function SimpleAppScreen({ appId, onBack }) {
  const meta = CONTENT[appId?.id] || { title: 'Приложение', text: 'Ничего интересного здесь нет.' };
  const AppIconComp = appId?.Icon;

  return (
    <div className="relative w-full h-full bg-zinc-950 text-white font-sans flex flex-col overflow-hidden">
      <div className="flex items-center gap-2 px-3 py-2.5 h-14 flex-shrink-0 border-b border-zinc-800">
        <button
          onClick={onBack}
          className="w-9 h-9 rounded-full hover:bg-zinc-800 flex items-center justify-center text-blue-500 transition-colors"
        >
          <ChevronLeft size={22} />
        </button>
        <div className="text-base font-semibold">{meta.title}</div>
      </div>

      <div className="flex-1 flex flex-col items-center justify-center gap-3 px-8 text-center">
        {AppIconComp && (
          <div className={`w-16 h-16 ${appId.bgClass} rounded-[22px] flex items-center justify-center opacity-70`}>
            <AppIconComp className="text-white" size={30} strokeWidth={1.5} />
          </div>
        )}
        <div className="text-sm text-zinc-500">{meta.text}</div>
      </div>
    </div>
  );
}
