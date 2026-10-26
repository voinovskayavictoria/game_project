import { useState } from 'react';
import {
  MessageSquare, Phone, Image, Mail, Globe, Folder, Settings, Camera, Search, FileText, Map as MapIcon,
} from 'lucide-react';

const APPS = [
  { id: 'messages', Icon: MessageSquare, name: 'Сообщения', bgClass: 'bg-blue-500' },
  { id: 'phone', Icon: Phone, name: 'Телефон', bgClass: 'bg-green-500' },
  { id: 'gallery', Icon: Image, name: 'Галерея', bgClass: 'bg-orange-500' },
  { id: 'mail', Icon: Mail, name: 'Почта', bgClass: 'bg-red-500' },
  { id: 'browser', Icon: Globe, name: 'Интернет', bgClass: 'bg-indigo-500' },
  { id: 'files', Icon: Folder, name: 'Мои файлы', bgClass: 'bg-yellow-500' },
  { id: 'notes', Icon: FileText, name: 'Заметки', bgClass: 'bg-amber-600' },
  { id: 'maps', Icon: MapIcon, name: 'Карты', bgClass: 'bg-teal-500' },
  { id: 'settings', Icon: Settings, name: 'Настройки', bgClass: 'bg-gray-600' },
  { id: 'camera', Icon: Camera, name: 'Камера', bgClass: 'bg-purple-500' },
];

const DOCK_APPS = [
  { id: 'phone', Icon: Phone, bgClass: 'bg-green-500' },
  { id: 'messages', Icon: MessageSquare, bgClass: 'bg-blue-500' },
  { id: 'browser', Icon: Globe, bgClass: 'bg-indigo-500' },
  { id: 'files', Icon: Folder, bgClass: 'bg-yellow-500' },
];

const AppIcon = ({ app, onOpen }) => {
  const { Icon, name, bgClass } = app;
  return (
    <button
      onClick={() => onOpen(app.id)}
      className="flex flex-col items-center justify-center w-20 h-24 active:scale-95 transition-transform duration-100"
    >
      <div className={`w-14 h-14 ${bgClass} rounded-[20px] flex items-center justify-center shadow-lg`}>
        <Icon className="text-white" size={28} strokeWidth={1.5} />
      </div>
      <span className="app-label text-white mt-2 truncate w-full text-center px-1 drop-shadow-md">
  {name}
</span>
    </button>
  );
};

export default function HomeScreen({ onOpenApp }) {
  const [notifications] = useState(3);

  return (
    <div className="relative w-full h-full text-white font-sans flex flex-col justify-between p-4 overflow-hidden">

      {/* Фон — обои */}
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: "url('/wallpaper.jpg')" }}
      />
      {/* Затемнение для читаемости */}
      <div className="absolute inset-0 bg-black/35" />

      <div className="relative w-full pt-2 px-2">
        <div className="w-full h-12 bg-zinc-900/60 backdrop-blur-md rounded-2xl flex items-center px-4 gap-3 text-zinc-300 border border-white/10">
          <Search size={18} className="text-zinc-400" />
          <span className="text-sm font-light">Поиск</span>
        </div>
      </div>
      
      <div className="relative grid grid-cols-4 gap-y-4 gap-x-2 px-1 text-center mt-3 mb-auto">
        {APPS.map((app) => (
          <AppIcon key={app.id} app={app} onOpen={onOpenApp} />
        ))}
      </div>

      <div className="relative flex justify-center gap-1.5 mb-3">
        <div className="w-1.5 h-1.5 rounded-full bg-white"></div>
        <div className="w-1.5 h-1.5 rounded-full bg-white/40"></div>
        <div className="w-1.5 h-1.5 rounded-full bg-white/40"></div>
      </div>

      <div className="relative w-full flex justify-around px-2 pb-3">
        {DOCK_APPS.map((app) => {
          const { Icon, bgClass } = app;
          return (
            <button
              key={app.id}
              onClick={() => onOpenApp(app.id)}
              className={`w-14 h-14 ${bgClass} rounded-[20px] flex items-center justify-center shadow-lg active:scale-95 transition-transform relative`}
            >
              <Icon className="text-white" size={28} strokeWidth={1.5} />
              {app.id === 'messages' && notifications > 0 && (
                <div className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full text-[10px] flex items-center justify-center text-white font-bold">
                  {notifications}
                </div>
              )}
            </button>
          );
        })}
      </div>

      <div className="relative w-32 h-1 bg-white/40 rounded-full mx-auto mb-2"></div>
    </div>
  );
}