# -*- coding: utf-8 -*-

SITE = {
    "name": "ЧЁРНЫЙ КАКАО",
    "tagline": "Кофе, какао и немного тишины.",
    "instagram": "https://instagram.com/blackcacao",
    "email": "hello@black-cocoa.example",
    "phone": "+7 (000) 000-00-08",
    "address_new": "ул. Садовая, 17",
    "address_old": "ул. Лесная, 8",
    "city": "Москва",
    "opened_year": 2021,
    "moved_year": 2024,
    "hours": [
        ("Пн–Чт", "08:00 — 23:00"),
        ("Пт",    "08:00 — 02:00"),
        ("Сб",    "10:00 — 02:00"),
        ("Вс",    "10:00 — 22:00"),
    ],
}

EXTERNAL_LINKS = {
    "prime":  {"port": 5001, "name": "PRIME SYSTEMS"},
    "lumen":  {"port": 5002, "name": "LUMEN FORUM"},
    "haeil":  {"port": 5003, "name": "HAEIL & PARTNERS"},
    "vector": {"port": 5004, "name": "Vector Labs"},
    "orbit":  {"port": 5005, "name": "Orbit Data"},
    "c17arch":{"port": 5006, "name": "C-17 Archive"},
    "lebedeva":{"port": 5007, "name": "Мария Лебедева"},
}

MENU = [
    {
        "group": "Какао",
        "items": [
            {"name": "«17:04» — фирменное какао", "price": "320 ₽",
             "note": "Тёмный шоколад, корица, морская соль.",
             "signature": True},
            {"name": "Классическое какао", "price": "220 ₽"},
            {"name": "Какао с маршмеллоу", "price": "260 ₽"},
        ],
    },
    {
        "group": "Кофе",
        "items": [
            {"name": "Эспрессо", "price": "150 ₽"},
            {"name": "Капучино", "price": "240 ₽"},
            {"name": "Флэт-уайт", "price": "260 ₽"},
            {"name": "Фильтр", "price": "280 ₽"},
        ],
    },
    {
        "group": "Чай",
        "items": [
            {"name": "Чёрный с чабрецом", "price": "200 ₽"},
            {"name": "Облепиховый", "price": "240 ₽"},
        ],
    },
    {
        "group": "Десерты",
        "items": [
            {"name": "Брауни", "price": "220 ₽"},
            {"name": "Чизкейк", "price": "260 ₽"},
            {"name": "Тарт с грушей", "price": "280 ₽"},
        ],
    },
    {
        "group": "Выпечка",
        "items": [
            {"name": "Круассан", "price": "180 ₽"},
            {"name": "Синнабон", "price": "200 ₽"},
        ],
    },
]

NEWS = [
    {
        "slug": "thanks-18-09",
        "date": "18.09.2026",
        "title": "Спасибо всем, кто был вчера вечером!",
        "body": (
            "Небольшой вечер после закрытия ❤️\n\n"
            "Обязательно повторим. Следите за анонсами — "
            "подписывайтесь на наш Instagram."
        ),
        "photo": "img/guests-1809.jpg",
        "featured": True,
    },
    {
        "slug": "closed-tasting",
        "date": "15.09.2026",
        "title": "Закрытая дегустация нового меню",
        "body": "Вчера у нас прошла закрытая дегустация. Обновлённое меню — уже совсем скоро.",
    },
    {
        "slug": "friday-late",
        "date": "09.09.2026",
        "title": "Теперь по пятницам работаем до 02:00",
        "body": "Встречайте пятницу без спешки. Мы продлили часы работы.",
    },
    {
        "slug": "second-hall",
        "date": "02.09.2026",
        "title": "Мы обновили интерьер второго зала!",
        "body": "Мягкий свет, дерево, больше места для больших компаний.",
    },
    {
        "slug": "summer-end",
        "date": "20.08.2026",
        "title": "Прощаемся с летним меню",
        "body": "Холодный какао с мятой уходит до следующего года. Но у нас появился облепиховый чай.",
    },
]

EVENTS = [
    {"slug": "board-games", "date": "05.09.2026", "title": "Вечер настольных игр",
     "desc": "Раз в две недели собираемся за большим столом во втором зале."},
    {"slug": "music-night", "date": "12.09.2026", "title": "Музыкальный вечер",
     "desc": "Живой акустический сет. Вход свободный."},
    {"slug": "tasting-15", "date": "15.09.2026", "title": "Закрытая дегустация",
     "desc": "Пригласительные — среди подписчиков Instagram."},
    {
        "slug": "it-meetup-18",
        "date": "18.09.2026",
        "title": "IT Meetup",
        "desc": (
            "Неформальная встреча разработчиков и представителей "
            "технологических компаний."
        ),
        "note": "Список участников не публикуется. Только фотографии.",
        "photo": "img/guests-1809.jpg",
    },
    {"slug": "cinema-night", "date": "22.09.2026", "title": "Киноночь",
     "desc": "Показываем старое кино во втором зале с 23:00."},
]

STAFF = [
    {"name": "Анна", "role": "управляющая",
     "photo": "img/staff/anna.jpg"},
    {"name": "Игорь", "role": "шеф-бариста",
     "photo": "img/staff/igor.jpg"},
    {"name": "Марина", "role": "администратор",
     "photo": "img/staff/marina.jpg"},
    {
        "name": "Алексей",
        "role": "фотограф кафе",
        "photo": "img/staff/alexey.jpg",
        "instagram": "https://instagram.com/alexey.shoots",
    },
]

GALLERY = [
    {"file": "img/interior-1.jpg", "caption": "Основной зал"},
    {"file": "img/interior-2.jpg", "caption": "Второй зал"},
    {"file": "img/window.jpg", "caption": "Место у окна"},
    {"file": "img/entrance.jpg", "caption": "Вход со двора"},
    {"file": "img/sign.jpg", "caption": "Наша вывеска"},
    {"file": "img/coffee.jpg", "caption": "Капучино с какао-крошкой"},
    {"file": "img/dessert.jpg", "caption": "Брауни"},
    {"file": "img/guests-1809.jpg", "caption": "Небольшой вечер после закрытия ❤️",
     "date": "18.09.2026", "featured": True},
]

BOOKING_CONFIRMATION = {
    "ref": "BCC-1704",
    "date": "18.09.2026",
    "time": "22:00",
    "table": 17,
    "guests": 2,
    "note": "Столик №17, у окна.",
}