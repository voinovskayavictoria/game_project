import { useState, useEffect, useRef } from 'react';
import { ChevronLeft, Send } from 'lucide-react';

export default function Messenger({ onBack }) {
  const [messages, setMessages] = useState([]);
  const [options, setOptions] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [showInput, setShowInput] = useState(false);
  const [state, setState] = useState(0);
  const [wrongAttempts, setWrongAttempts] = useState(0);
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Инициализация: первое сообщение от Маши
  useEffect(() => {
    setTimeout(() => {
      setIsTyping(true);
      setTimeout(() => {
        setIsTyping(false);
        addBotMessage('Кто это? Если вы из H&P — я уже всё удалила. Больше мне не пишите.');
        showInitialOptions();
      }, 700);
    }, 400);
  }, []);

  const addMessage = (text, isUser) => {
    setMessages(prev => [...prev, { text, isUser, timestamp: new Date() }]);
  };

  const addBotMessage = (text) => {
    addMessage(text, false);
  };

  const addBotSays = (text, delay) => {
    setTimeout(() => {
      setIsTyping(true);
      setTimeout(() => {
        setIsTyping(false);
        addBotMessage(text);
      }, 700);
    }, delay);
  };

  const showInitialOptions = () => {
    setOptions([
      { text: 'Я не из H&P. Я журналист, хочу помочь.', onClick: answerJournalist },
      { text: 'Слушай, мне нужна информация. Быстро.', onClick: answerAggressive },
      { text: 'Простите за беспокойство. Я ошибся номером.', onClick: answerWrongNumber },
    ]);
  };

  const answerJournalist = () => {
    addMessage('Я не из H&P. Я журналист, хочу помочь.', true);
    setOptions([]);
    addBotSays('Журналист? Хм. Они тоже так говорили. Как мне убедиться, что вы не они?', 1300);
    setTimeout(() => {
      setOptions([
        { text: 'Я знаю про C-17 и про то, что случилось с PRIME.', onClick: answerKnowsC17 },
        { text: 'У меня есть документы из HAEIL & PARTNERS.', onClick: answerHasDocs },
        { text: 'Я просто хочу правду. Как и вы.', onClick: answerJustTruth },
      ]);
    }, 2600);
  };

  const answerAggressive = () => {
    addMessage('Слушай, мне нужна информация. Быстро.', true);
    setOptions([]);
    addBotSays('Вот теперь я точно вижу, что вы из H&P. Угрозы, давление. Всё как всегда.', 1300);
    addBotSays('Я блокирую этот контакт. Не пишите мне больше.', 2900);
    setTimeout(() => {
      setOptions([
        { text: '🔄  Начать диалог заново', onClick: resetDialog },
      ]);
    }, 4000);
  };

  const answerWrongNumber = () => {
    addMessage('Простите за беспокойство. Я ошибся номером.', true);
    setOptions([]);
    addBotSays('Тогда зачем вы написали именно мне? Я не верю в совпадения.', 1300);
    addBotSays('Больше не пишите.', 2900);
    setTimeout(() => {
      setOptions([
        { text: '🔄  Начать диалог заново', onClick: resetDialog },
      ]);
    }, 4000);
  };

  const answerKnowsC17 = () => {
    addMessage('Я знаю про C-17 и про то, что случилось с PRIME.', true);
    setOptions([]);
    addBotSays('Откуда вы знаете это название? Его не должно быть в открытых источниках.', 1300);
    addBotSays('Ладно. Если вы правда копаете — назовите фамилию основателя PRIME SYSTEMS. Того, кого они кинули.', 2900);
    setTimeout(() => {
      showInputField();
    }, 4000);
  };

  const answerHasDocs = () => {
    addMessage('У меня есть документы из HAEIL & PARTNERS.', true);
    setOptions([]);
    addBotSays('Документы? У H&P сотни юристов. Они могли подослать кого угодно.', 1300);
    addBotSays('Докажите, что вы не их человек. Назовите фамилию основателя PRIME SYSTEMS.', 2900);
    setTimeout(() => {
      showInputField();
    }, 4000);
  };

  const answerJustTruth = () => {
    addMessage('Я просто хочу правду. Как и вы.', true);
    setOptions([]);
    addBotSays('Красивые слова. Но слова — это дешево. Мне нужны доказательства.', 1300);
    addBotSays('Назовите фамилию основателя PRIME SYSTEMS. Если вы правда в теме — вы знаете.', 2900);
    setTimeout(() => {
      showInputField();
    }, 4000);
  };

  const showInputField = () => {
    setState(2);
    setShowInput(true);
    setOptions([]);
  };

  const checkProof = () => {
    const text = inputValue.trim();
    
    if (text.toLowerCase().includes('соколов')) {
      addMessage(text, true);
      setState(3);
      setShowInput(false);
      setInputValue('');
      setOptions([]);

      addBotSays('Ладно... Похоже, вы реально копаете. Соколов. Да, это он.', 1300);
      addBotSays('Слушайте, они заставили меня удалить оригинал статьи и пригрозили судом.', 2900);
      addBotSays('Но я сохранила теневую копию на Teletype. Нигде это не светите.', 4500);
      addBotSays('Вот ссылка: teletype.in/@m_lebedeva/c17_investigation', 6100);
      setTimeout(() => {
        setOptions([
          { text: 'Спасибо. Я обещаю, что не подведу.', onClick: answerThanks },
          { text: 'Почему вы не опубликовали это снова?', onClick: answerWhy },
        ]);
      }, 7200);
    } else {
      setWrongAttempts(prev => prev + 1);
      addMessage(text || '(пусто)', true);

      if (wrongAttempts >= 2) {
        addBotSays('Вы не знаете даже этого. Вы точно не тот, за кого себя выдаёте.', 1300);
        addBotSays('Я блокирую контакт. Прощайте.', 2900);
        setTimeout(() => {
          setOptions([
            { text: '🔄  Начать диалог заново', onClick: resetDialog },
          ]);
          setShowInput(false);
        }, 4000);
      } else {
        addBotSays('Это не то имя. Подумайте ещё. Это человек, чья компания создала C-17.', 1300);
        setTimeout(() => {
          setShowInput(true);
          setInputValue('');
        }, 2600);
      }
    }
  };

  const answerThanks = () => {
    addMessage('Спасибо. Я обещаю, что не подведу.', true);
    setOptions([]);
    addBotSays('Просто будьте осторожны. Они везде. Удачи.', 1300);
  };

  const answerWhy = () => {
    addMessage('Почему вы не опубликовали это снова?', true);
    setOptions([]);
    addBotSays('Потому что у них лучшие юристы в стране. Я устала бояться.', 1300);
    addBotSays('Просто будьте осторожны. Они везде. Удачи.', 2900);
  };

  const resetDialog = () => {
    setState(0);
    setWrongAttempts(0);
    setMessages([]);
    setOptions([]);
    setShowInput(false);
    setInputValue('');
    setIsTyping(false);

    setTimeout(() => {
      setIsTyping(true);
      setTimeout(() => {
        setIsTyping(false);
        addBotMessage('Кто это? Если вы из H&P — я уже всё удалила. Больше мне не пишите.');
        showInitialOptions();
      }, 700);
    }, 400);
  };

  return (
    <div className="relative w-full h-full bg-zinc-950 text-white font-sans flex flex-col overflow-hidden">
      
      {/* Шапка */}
      <div className="flex items-center gap-3 px-3 py-3 h-16 bg-zinc-950 border-b border-zinc-800">
        <button
          onClick={onBack}
          className="w-10 h-10 rounded-full bg-transparent hover:bg-zinc-800 flex items-center justify-center text-blue-500 transition-colors"
        >
          <ChevronLeft size={24} />
        </button>
        <div className="w-10 h-10 bg-zinc-700 rounded-full flex items-center justify-center text-sm flex-shrink-0">
          👤
        </div>
        <div className="flex-1">
          <div className="text-base font-semibold text-white">@m_lebedeva_press</div>
          <div className="text-xs text-zinc-400">была недавно</div>
        </div>
      </div>

      {/* Область чата */}
      <div className="flex-1 overflow-y-auto flex flex-col gap-1 p-2 bg-zinc-950">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xs ${msg.isUser ? 'mr-2' : 'ml-2'}`}>
              <div className={`rounded-2xl px-4 py-2 ${msg.isUser ? 'bg-blue-500 text-white' : 'bg-zinc-800 text-white'}`}>
                <div className="text-sm leading-relaxed break-words">{msg.text}</div>
              </div>
              <div className={`text-xs text-zinc-500 mt-1 ${msg.isUser ? 'text-right' : 'text-left'} px-2`}>
                {msg.timestamp.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex justify-start">
            <div className="ml-2 bg-zinc-800 rounded-2xl px-4 py-2">
              <div className="flex gap-1">
                <span className="text-xs text-zinc-400 animate-pulse">●</span>
                <span className="text-xs text-zinc-400 animate-pulse" style={{ animationDelay: '0.2s' }}>●</span>
                <span className="text-xs text-zinc-400 animate-pulse" style={{ animationDelay: '0.4s' }}>●</span>
              </div>
            </div>
          </div>
        )}

        <div ref={chatEndRef}></div>
      </div>

      {/* Панель вариантов или ввода */}
      <div className="bg-zinc-900 border-t border-zinc-800 p-3 max-h-80 overflow-y-auto flex flex-col gap-2">
        {showInput && (
          <div className="flex flex-col gap-2">
            <label className="text-xs text-zinc-400 px-2">Введите фамилию основателя PRIME SYSTEMS</label>
            <div className="flex gap-2 px-1">
              <input
                type="text"
                placeholder="Фамилия..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && checkProof()}
                autoFocus
                className="flex-1 px-4 py-2 bg-zinc-800 border border-zinc-700 rounded-2xl text-white text-sm placeholder-zinc-500 focus:outline-none focus:border-blue-500"
              />
              <button
                onClick={checkProof}
                className="w-11 h-11 bg-blue-500 rounded-full flex items-center justify-center text-white hover:bg-blue-600 transition-colors active:scale-95"
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        )}

        {!showInput && options.map((opt, i) => (
          <button
            key={i}
            onClick={opt.onClick}
            className="w-full px-4 py-3 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 rounded-2xl text-white text-sm text-left transition-colors active:scale-95"
          >
            {opt.text}
          </button>
        ))}
      </div>
    </div>
  );
}
