// src/data.js
export const MILANA_RESUME = {
  name: 'Милана Макарова',
  position: 'Менеджер по работе с персоналом (HR)',
  company: 'PRIME SYSTEMS',
  experience: '5 лет',
  skills: ['Подбор персонала', 'Организация мероприятий', 'Коммуникация', 'Переговоры'],
  phone: '+7 (999) 123-4567',
  email: 'milana.makarova@primesystems.io',
  birthdate: '15.03.1995',
};

export const SECURITY_QUESTIONS = [
  { q: 'На какой должности работает Милана?', a: 'менеджер' },
  { q: 'Сколько лет опыта?', a: '5' },
  { q: 'Год рождения?', a: '1995' },
];

export const THREADS = [
  {
    id: 'lev',
    name: 'Лев 💙',
    avatar: '🧑🏻',
    color: 'bg-sky-500',
    unread: false,
    messages: [
      { who: 'them', text: 'Ты как? Весь день пишу и не отвечаешь 😞', time: '21:10' },
      { who: 'me', text: 'Извини, весь день на нервах. Не могу объяснить', time: '21:14' },
      { who: 'them', text: 'Из-за передачи проекта Орбите? У нас тоже сейчас дурдом с OD-17', time: '21:16' },
      { who: 'me', text: 'Лев, давай не в переписке. Увидимся вечером?', time: '21:18' },
      { who: 'them', text: 'Давай, но не у тебя. Мало ли кто увидит', time: '21:19' },
      { who: 'them', text: 'Знаешь, я иногда думаю — сколько нам ещё скрываться', time: '22:40' },
      { who: 'me', text: 'Пока всё не уляжется — так надо. Ты же сам понимаешь риски', time: '22:45' },
      { who: 'them', text: 'Понимаю. Просто устал всем врать, что мы «просто коллеги»', time: '22:47' },
      { who: 'them', text: 'Будь осторожна с Германом, он что-то подозревает', time: '23:02' },
      { who: 'me', text: 'Он всегда всё подозревает, он такой', time: '23:05' },
      { who: 'them', text: 'Не в этот раз. Спрашивал, почему я так часто торчу у твоего подъезда', time: '23:07' },
    ],
  },
  {
    id: 'masha',
    name: 'Маша Лебедева',
    avatar: '📰',
    color: 'bg-zinc-600',
    unread: true,
    messages: [
      { who: 'them', text: 'Милана, я знаю про OD-17. Помоги мне разобраться.', time: '23:45' },
      { who: 'them', text: 'Ты в опасности. Они хотят тебя сдать.', time: '00:12' },
      { who: 'them', text: 'Я готова помочь. Встретимся?', time: '00:30' },
      { who: 'me', text: 'Я расскажу тебе ВСЁ. Но никому больше.', time: '01:15' },
      { who: 'them', text: '[Документ: C17_OD17_TRUTH.PDF]', time: '02:30' },
      { who: 'them', text: 'Спасибо. Это спасёт людей.', time: '02:45' },
      { who: 'them', text: 'Милана?', time: '08:00' },
      { who: 'them', text: 'Ответь пожалуйста...', time: '10:30' },
      { who: 'them', text: 'Милана, ты где? 😟', time: '15:45' },
    ],
  },
  {
    id: 'german',
    name: 'Герман',
    avatar: '😐',
    color: 'bg-orange-600',
    unread: false,
    messages: [
      { who: 'them', text: 'Слышал, твоя контора продала мой проект Орбите. Красиво.', time: '14:02' },
      { who: 'me', text: 'Герман, я не принимаю такие решения, ты же знаешь', time: '14:05' },
      { who: 'them', text: 'Ну конечно. HR никогда ничего не решает, ага', time: '14:06' },
      { who: 'them', text: 'Три года на C-17 положил, а меня даже на созвон не позвали', time: '14:10' },
      { who: 'me', text: 'Мне жаль, что так вышло. Правда', time: '14:12' },
      { who: 'them', text: 'Оставь жалость себе. Просто передай начальству, что я всё делал по правилам — в отличие от них', time: '14:15' },
      { who: 'them', text: 'И да, молчать не собираюсь, если начнут вешать на меня косяки Орбиты', time: '14:16' },
      { who: 'me', text: 'Никто на тебя ничего не вешает', time: '14:18' },
      { who: 'them', text: 'Посмотрим.', time: '14:19' },
    ],
  },
  {
    id: 'mom',
    name: 'Мама ❤️',
    avatar: '👩🏻',
    color: 'bg-pink-500',
    unread: false,
    messages: [
      { who: 'them', text: 'Милана, ты ужинала?', time: '19:02' },
      { who: 'me', text: 'Мам, ем нормально, не переживай', time: '19:10' },
      { who: 'them', text: 'Зайди в субботу, отец соскучился', time: '19:12' },
      { who: 'me', text: 'Хорошо, постараюсь', time: '19:15' },
      { who: 'them', text: 'И запишись уже к врачу, сколько можно тянуть', time: '19:16' },
    ],
  },
  {
    id: 'nastya',
    name: 'Настя',
    avatar: '💁🏼‍♀️',
    color: 'bg-fuchsia-500',
    unread: false,
    messages: [
      { who: 'them', text: 'Едем в субботу на день рождения к Роме?', time: '12:00' },
      { who: 'me', text: 'Ой, надо подумать, неделя тяжёлая была', time: '12:05' },
      { who: 'them', text: 'Да ладно, развеешься! Там будет твой бывший, кстати 👀', time: '12:07' },
      { who: 'me', text: 'Именно поэтому надо подумать 😂', time: '12:09' },
      { who: 'them', text: '🤣🤣🤣 ну как знаешь', time: '12:10' },
    ],
  },
  {
    id: 'hr-chat',
    name: 'HR | Prime Systems',
    avatar: '🏢',
    color: 'bg-indigo-500',
    unread: false,
    messages: [
      { who: 'them', text: 'Напоминание: собрание отдела в 15:00, конференц-зал 2', time: '09:00' },
      { who: 'them', text: 'Не забудьте сдать отчёты по подбору за квартал', time: '09:03' },
      { who: 'them', text: 'Милана, скинь резюме кандидатов на почту', time: '11:20' },
      { who: 'me', text: 'Скинула, проверьте папку "Кандидаты Q3"', time: '11:35' },
    ],
  },
  {
    id: 'delivery',
    name: 'Яндекс Еда',
    avatar: '🍔',
    color: 'bg-yellow-500',
    unread: false,
    messages: [
      { who: 'them', text: 'Ваш заказ #48291 передан курьеру', time: '13:40' },
      { who: 'them', text: 'Заказ доставлен! Приятного аппетита 🎉', time: '14:05' },
      { who: 'them', text: 'Как вам блюда? Оцените заказ ⭐⭐⭐⭐⭐', time: '15:00' },
    ],
  },
  {
    id: 'salon',
    name: 'Салон красоты «Нежность»',
    avatar: '💅',
    color: 'bg-rose-400',
    unread: false,
    messages: [
      { who: 'them', text: 'Милана, напоминаем: у вас запись на маникюр завтра в 18:00', time: '10:00' },
    ],
  },
];

export const PHONE_CALLS = [
  { from: 'Лев 💙', time: '23:10', duration: '42m 10s', type: 'outgoing' },
  { from: 'Герман', time: '14:22', missed: true, type: 'incoming' },
  { from: 'Маша Лебедева', time: '09:15', missed: true, type: 'incoming' },
  { from: 'Маша Лебедева', time: '12:00', missed: true, type: 'incoming' },
  { from: 'Мама ❤️', time: '19:30', missed: true, type: 'incoming' },
  { from: 'Настя', time: '11:05', duration: '3m 20s', type: 'incoming' },
  { from: 'Лев 💙', time: '01:02', duration: '15m 44s', type: 'incoming' },
  { from: 'Салон красоты «Нежность»', time: '10:00', duration: '0m 40s', type: 'outgoing' },
];

export const GALLERY_FILES = [
  { id: 1, url: '/cat_bonya.jpg', type: 'personal' },
  { id: 2, url: '/gym_selfie.jpg', type: 'personal' },
  { id: 3, url: '/nastya_bday.jpg', type: 'personal' },
  { id: 4, url: '/sunset_balcony.jpg', type: 'personal' },
  { id: 5, url: '/telegram_1.jpg', type: 'screenshot' },
  { id: 6, url: '/telegram_2.jpg', type: 'screenshot' },
  { id: 7, url: '/park_lev.jpg', type: 'deleted' },
  { id: 8, url: '/cafe_lev.jpg', type: 'deleted' },
  { id: 9, url: '/food_sushi.jpg', type: 'personal' },
  { id: 10, url: '/od17_chat.jpg', type: 'screenshot' },
];

export const NOTIFICATIONS = [
  { app: 'Telegram', icon: '✈️', text: '@m_lebedeva_press: новое сообщение', time: '10:30', threadId: 'masha' },
  { app: 'Telegram', icon: '✈️', text: 'Лев: "Ты как? 😞"', time: '21:10', threadId: 'lev' },
  { app: 'Instagram', icon: '📷', text: 'nastya_k и ещё 12 оценили ваше фото', time: '09:12' },
  { app: 'VK', icon: '🔵', text: 'Новое сообщение от Насти', time: '12:00', threadId: 'nastya' },
  { app: 'Яндекс Еда', icon: '🍔', text: 'Заказ #48291 доставлен', time: '14:05', threadId: 'delivery' },
  { app: 'Салон «Нежность»', icon: '💅', text: 'Запись на маникюр завтра в 18:00', time: '10:00', threadId: 'salon' },
  { app: 'Календарь', icon: '📅', text: 'Приём у врача — завтра в 10:00', time: '19:16' },
  { app: 'Система', icon: '🔋', text: 'Батарея разряжается (12%)', time: '05:15' },
];