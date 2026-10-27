import React from 'react';

export default function BrokenPdfModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="absolute inset-0 bg-black/80 flex items-center justify-center p-3 z-50">
      <div className="bg-zinc-100 text-black w-full h-[90%] rounded-xl shadow-2xl flex flex-col overflow-hidden">
        
        {/* Шапка PDF */}
        <div className="bg-zinc-300 p-3 flex justify-between items-center border-b border-zinc-400">
          <span className="font-mono text-sm font-bold text-red-600">⚠️ C17_OD17_TRUTH.PDF [ПОВРЕЖДЕН]</span>
          <button 
            onClick={onClose}
            className="text-zinc-600 hover:text-black font-bold px-2 text-xl cursor-pointer"
          >
            ✕
          </button>
        </div>

       {/* Тело "документа" */}
<div className="p-6 overflow-y-auto font-mono text-sm leading-relaxed flex-1 bg-zinc-50 text-justify">
  
  <div className="text-center mb-6 text-zinc-500">
    --- НАЧАЛО ФРАГМЕНТА АУДИОЗАПИСИ / ЧЕРНОВИК ИНТЕРВЬЮ ---
  </div>

  <p className="mb-3"><strong className="text-blue-800">М. Лебедева:</strong> Милана, как ты вообще оказалась в этой схеме? В OD-17 не попадают случайно.</p>
  
  <p className="mb-3">
    <strong className="text-red-800">Милана:</strong> Туда на работу без связей не попасть... Мне помог один парень устроиться. У меня были огромные проблемы с деньгами, долги. Я думала, это просто логистика, HR. Обычный офис. <span className="bg-zinc-400 text-zinc-400 select-none">▓▓▓▓▓▓▓ ▓▓▓▓</span> я не знала, чем они на самом деле занимаются, пока не увидела накладные.
  </p>

  <p className="mb-3"><strong className="text-blue-800">М. Лебедева:</strong> Этот парень, который тебя устроил... Кто он? И чем конкретно ты занималась?</p>
  
  <p className="mb-3">
    <strong className="text-red-800">Милана:</strong> Он... <span className="bg-zinc-400 text-zinc-400 select-none">▓▓▓▓▓▓▓</span> в компании. Мы начали встречаться в 23-м. Он классный, он не такой как они. У него просто работа мутная, техническая. Он DevOps. Он сказал, что это просто «серые» схемы, но деньги быстрые. Я занималась «персоналом». Искала девушек для <span className="bg-zinc-400 text-zinc-400 select-none">▒▒▒▒▒▒▒▒▒▒▒▒</span>. Я не знала, что их потом переправляют! Я думала, это <span className="bg-zinc-400 text-zinc-400 select-none">▓▓▓▓▓▓▓</span>  или что-то в этом роде. <span className="bg-zinc-400 text-zinc-400 select-none">▓▓▓▓▓</span> это было ужасно.
  </p>

  <p className="mb-3"><strong className="text-blue-800">М. Лебедева:</strong> А какую роль во всем этом играл Соколов? Он просто не справился с контролем над проектом, или сознательно передал данные?</p>
  
  <p className="mb-3">
    <strong className="text-red-800">Милана:</strong> Соколов? Он... <span className="bg-zinc-400 text-zinc-400 select-none">▓▓▓▓▓▓▓</span> не справился? Нет. Он не идиот. С-17 передали не просто так. 17 апреля 2019 года была сделка. Соколова вынудили, или он просто продался. За этим стоит... <span className="bg-zinc-400 text-zinc-400 select-none">▓▓▓▓▓▓▓</span> <em className="text-zinc-500">(звук помех)</em> ...Orbit Data. Но Лев тут ни при чем, он просто чинит их сервера!
  </p>

  <p className="mb-3"><strong className="text-blue-800">М. Лебедева:</strong> Подожди. Orbit Data? А как же их директор, Алексей Мельников? Он в курсе?</p>

  <p className="mb-3">
    <strong className="text-red-800">Милана:</strong> Мельников? <em className="text-zinc-500">(вздыхает)</em> Я видела его пару раз. Он выглядит как обычный бизнесмен. Но в компании постоянно какие-то терки. Лев говорил, что у Мельникова давний конфликт с Климовым. Еще из прошлого их проекта. Климов консультировал HAEIL & Partners, и у него везде свои люди. 
  </p>

  <p className="mb-3">
    <strong className="text-red-800">Милана:</strong> Когда я сказала Льву, что больше не могу этим заниматься и хочу уйти, он очень испугался. Сказал, что «просто уволиться» не получится, что я слишком много знаю. Я сначала думала, что он преувеличивает. Но потом мне начали поступать странные звонки. Молчание в трубку. Сообщения с незнакомых номеров. Лев сказал, что это «они» проверяют, не сболтнула ли я лишнего. Он обещал что-нибудь придумать. Обещал меня защитить.
  </p>

  <p className="mb-4 text-zinc-600 italic border-l-4 border-red-500 pl-4 my-6">
    [ОШИБКА ЧТЕНИЯ СЕКТОРА: КОНЕЦ ФАЙЛА ПОВРЕЖДЕН. ДАЛЬНЕЙШИЙ ТЕКСТ НЕВОЗМОЖНО ВОССТАНОВИТЬ]
  </p>

</div>
      </div>
    </div>
  );
}