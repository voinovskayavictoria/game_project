import { ChevronLeft, Wifi, AlertCircle } from 'lucide-react';

export default function BrowserError({ onBack }) {
  return (
    <div className="relative w-full h-full bg-zinc-950 text-white font-sans flex flex-col">
      
      {/* Адресная строка */}
      <div className="bg-zinc-900 border-b border-zinc-800 px-3 pb-3 pt-8 flex items-center gap-2">
        <button
          onClick={onBack}
          className="text-blue-500 hover:text-blue-400 transition-colors"
        >
          <ChevronLeft size={20} />
        </button>
        <div className="flex-1 bg-zinc-800 rounded-lg px-3 py-2 text-xs text-zinc-400 truncate">
        </div>
      </div>

      {/* Основной контент ошибки */}
      <div className="flex-1 flex flex-col items-center justify-center p-4">
        
        <AlertCircle size={64} className="text-yellow-500 mb-4" />
        
        <h1 className="text-2xl font-bold mb-2 text-center">Нет подключения</h1>
        
        <p className="text-sm text-zinc-400 text-center mb-6">
          Не удалось подключиться к интернету. Проверьте соединение Wi-Fi или мобильную сеть.
        </p>

        <div className="w-full max-w-sm bg-zinc-900 rounded-2xl p-4 border border-zinc-800 mb-6">
          <div className="flex items-center gap-3 mb-3">
            <Wifi size={20} className="text-zinc-500" />
            <span className="text-sm font-semibold">Wi-Fi отключен</span>
          </div>
        </div>

      </div>
    </div>
  );
}
