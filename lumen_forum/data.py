# -*- coding: utf-8 -*-

SITE = {
    "name": "LUMEN FORUM",
    "tagline": "Технологии. Люди. Будущее.",
    "founded": 2015,
    "description": (
        "Ежегодный технологический форум, объединяющий компании, "
        "исследователей и независимых экспертов."
    ),
}

# ------------------------------------------------------------------
# Ссылки на другие сайты игры.
# Хост подставляется динамически через context_processor (HOST).
# Здесь только порт и подпись.
# ------------------------------------------------------------------
EXTERNAL_LINKS = {
    "prime":   {"port": 5001, "name": "PRIME SYSTEMS"},
    "haeil":   {"port": 5003, "name": "Haeil & Partners"},
    "vector":  {"port": 5004, "name": "Vector Labs"},
    "orbit":   {"port": 5005, "name": "Orbit Data"},
}

# ------------------------------------------------------------------
# УЧАСТНИКИ
# ------------------------------------------------------------------
PARTICIPANTS = [
    {
        "slug": "pavel-sokolov",
        "name": "Павел Соколов",
        "role": "CEO",
        "company": "PRIME SYSTEMS",
        "years": [2019, 2020, 2021, 2023, 2024],
        "photo": "img/participants/sokolov.jpg",
        "bio": "Публичный представитель PRIME SYSTEMS, постоянный участник форума.",
        "external": "prime",
        "featured": True,
    },
    {
        "slug": "anna-voronova",
        "name": "Анна Воронова",
        "role": "CTO",
        "company": "PRIME SYSTEMS",
        "years": [2019, 2020, 2021, 2022, 2024],
        "photo": "img/participants/voronova.jpg",
        "bio": "Технический директор PRIME SYSTEMS, спикер секции безопасности.",
        "external": "prime",
        "featured": True,
    },
    {
        "slug": "maxim-orlov",
        "name": "Максим Орлов",
        "role": "COO",
        "company": "PRIME SYSTEMS",
        "years": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
        "photo": "img/participants/orlov.jpg",
        "bio": "Операционный директор PRIME SYSTEMS, куратор партнёрской программы форума.",
        "external": "prime",
        "featured": True,
    },
    {
        "slug": "han-jae-won",
        "name": "Хан Джэ Вон",
        "role": "Project Director",
        "company": "Orbit Data",
        "years": [2020, 2021, 2022, 2023],
        "photo": "img/participants/han.jpg",
        "bio": (
            "Руководитель проектов Orbit Data. Ранее работал в "
            "Vector Labs. Участник закрытых технических секций."
        ),
        "external": "orbit",
        "featured": True,
    },
    {
        "slug": "chong-woo-jin",
        "name": "Чон У Джин",
        "role": "Technology Consultant",
        "company": "Independent",
        "years": [2019, 2020, 2021, 2022, 2025],
        "photo": "img/participants/chong.jpg",
        "bio": (
            "Независимый технологический консультант. "
            "Специализация — закрытые коммуникационные системы."
        ),
        "external": None,
        "featured": True,
    },
    {
        "slug": "yuri-belov",
        "name": "Юрий Белов",
        "role": "Software Engineer",
        "company": "Vector Labs",
        "years": [2019, 2020, 2021],
        "photo": "img/participants/belov.jpg",
        "bio": "Инженер-разработчик. Ранее — PRIME SYSTEMS.",
        "external": "vector",
        "featured": True,
    },

    # --- Обычные участники (чтобы сайт выглядел живым) ---
    {"slug": "olga-kuznetsova", "name": "Ольга Кузнецова", "role": "Marketing Director",
     "company": "PRIME SYSTEMS", "years": [2022, 2023, 2024],
     "photo": "img/participants/kuznetsova.jpg", "external": "prime", "featured": False},
    {"slug": "sergey-nikitin", "name": "Сергей Никитин", "role": "Project Manager",
     "company": "PRIME SYSTEMS", "years": [2023, 2024],
     "photo": "img/participants/nikitin.jpg", "external": "prime", "featured": False},
    {"slug": "irina-volkova", "name": "Ирина Волкова", "role": "QA Lead",
     "company": "PRIME SYSTEMS", "years": [2022, 2024],
     "photo": "img/participants/volkova.jpg", "external": "prime", "featured": False},
    {"slug": "andrey-lebedev", "name": "Андрей Лебедев", "role": "Data Scientist",
     "company": "Orbit Data", "years": [2021, 2022, 2023],
     "photo": "img/participants/lebedev.jpg", "external": "orbit", "featured": False},
    {"slug": "ekaterina-kim", "name": "Екатерина Ким", "role": "Legal Counsel",
     "company": "Haeil & Partners", "years": [2020, 2021, 2022],
     "photo": "img/participants/kim.jpg", "external": "haeil", "featured": False},
    {"slug": "dmitry-volkov", "name": "Дмитрий Волков", "role": "Researcher",
     "company": "Vector Labs", "years": [2019, 2020],
     "photo": "img/participants/volkov.jpg", "external": "vector", "featured": False},
    {"slug": "mikhail-sorokin", "name": "Михаил Сорокин", "role": "CTO",
     "company": "Independent", "years": [2021, 2022],
     "photo": "img/participants/sorokin.jpg", "external": None, "featured": False},
]

# ------------------------------------------------------------------
# СПИКЕРЫ
# ------------------------------------------------------------------
SPEAKERS = [
    {
        "name": "Павел Соколов",
        "role": "CEO PRIME SYSTEMS",
        "talk": "Будущее корпоративных технологий",
        "year": 2021,
        "photo": "img/participants/sokolov.jpg",
    },
    {
        "name": "Анна Воронова",
        "role": "CTO PRIME SYSTEMS",
        "talk": "Безопасность цифровых систем",
        "year": 2021,
        "photo": "img/participants/voronova.jpg",
    },
    {
        "name": "Чон У Джин",
        "role": "Technology Consultant",
        "talk": "Закрытые коммуникационные системы",
        "year": 2021,
        "photo": "img/participants/chong.jpg",
    },
    {
        "name": "Хан Джэ Вон",
        "role": "Project Director, Orbit Data",
        "talk": "Аналитика распределённых данных",
        "year": 2022,
        "photo": "img/participants/han.jpg",
    },
]

# ------------------------------------------------------------------
# ПРОГРАММА ПО ГОДАМ
# ------------------------------------------------------------------
PROGRAM = {
    2019: {
        "theme": "Инфраструктура будущего",
        "participants": [
            "Павел Соколов (PRIME SYSTEMS)",
            "Анна Воронова (PRIME SYSTEMS)",
            "Максим Орлов (PRIME SYSTEMS)",
            "Чон У Джин (Independent)",
            "Юрий Белов (Vector Labs)",
        ],
        "highlights": [
            "Открытие секции корпоративных технологий",
            "Панель «Инфраструктура для распределённых команд»",
        ],
    },
    2020: {
        "theme": "Связность",
        "participants": [
            "Павел Соколов (PRIME SYSTEMS)",
            "Анна Воронова (PRIME SYSTEMS)",
            "Максим Орлов (PRIME SYSTEMS)",
            "Хан Джэ Вон (Orbit Data)",
            "Чон У Джин (Independent)",
            "Юрий Белов (Vector Labs)",
        ],
        "highlights": [
            "Секция «Аналитика в корпоративной среде»",
            "Закрытая техническая панель",
        ],
    },
    2021: {
        "theme": "Технологии. Люди. Будущее.",
        "participants": [
            "Павел Соколов (PRIME SYSTEMS)",
            "Анна Воронова (PRIME SYSTEMS)",
            "Максим Орлов (PRIME SYSTEMS)",
            "Хан Джэ Вон (Orbit Data)",
            "Чон У Джин (Independent)",
            "Юрий Белов (Vector Labs)",
            "Екатерина Ким (Haeil & Partners)",
            "Михаил Сорокин (Independent)",
        ],
        "highlights": [
            "Специальная панель: «Закрытые коммуникационные системы»",
            "Закрытая техническая секция — 17.04.2021",
            "Участники: PRIME SYSTEMS, Vector Labs, независимые консультанты",
        ],
        "note": "Самый насыщенный форум за всю историю LUMEN.",
    },
    2022: {
        "theme": "Данные и доверие",
        "participants": [
            "Анна Воронова (PRIME SYSTEMS)",
            "Максим Орлов (PRIME SYSTEMS)",
            "Хан Джэ Вон (Orbit Data)",
            "Чон У Джин (Independent)",
            "Андрей Лебедев (Orbit Data)",
            "Екатерина Ким (Haeil & Partners)",
        ],
        "highlights": ["Панель «Доверие в распределённых системах»"],
    },
    2023: {
        "theme": "Границы",
        "participants": [
            "Павел Соколов (PRIME SYSTEMS)",
            "Максим Орлов (PRIME SYSTEMS)",
            "Хан Джэ Вон (Orbit Data)",
            "Ольга Кузнецова (PRIME SYSTEMS)",
            "Андрей Лебедев (Orbit Data)",
            "Сергей Никитин (PRIME SYSTEMS)",
        ],
        "highlights": ["Круглый стол «Границы корпоративных систем»"],
    },
    2024: {
        "theme": "Следующий шаг",
        "participants": [
            "Павел Соколов (PRIME SYSTEMS)",
            "Анна Воронова (PRIME SYSTEMS)",
            "Максим Орлов (PRIME SYSTEMS)",
            "Ольга Кузнецова (PRIME SYSTEMS)",
            "Сергей Никитин (PRIME SYSTEMS)",
            "Ирина Волкова (PRIME SYSTEMS)",
        ],
        "highlights": ["Презентация новых продуктов PRIME"],
    },
    2025: {
        "theme": "Связи",
        "participants": [
            "Максим Орлов (PRIME SYSTEMS)",
            "Чон У Джин (Independent)",
        ],
        "highlights": ["Анонс форума 2026"],
    },
    2026: {
        "theme": "Технологии для людей",
        "participants": [],
        "highlights": ["Ближайший форум"],
        "upcoming": True,
    },
}

# ------------------------------------------------------------------
# ГАЛЕРЕЯ
# ------------------------------------------------------------------
GALLERY = [
    # --- Обычные фото ---
    {"file": "gallery/stage-2021.jpg",
     "caption": "Главная сцена LUMEN FORUM 2021.",
     "year": 2021, "tags": ["сцена"]},
    {"file": "gallery/audience-2021.jpg",
     "caption": "Зал во время пленарного заседания.",
     "year": 2021, "tags": ["зал"]},
    {"file": "gallery/booths-2021.jpg",
     "caption": "Стенды партнёров.",
     "year": 2021, "tags": ["стенды"]},
    {"file": "gallery/dinner-2021.jpg",
     "caption": "Вечерний приём.",
     "year": 2021, "tags": ["ужин"]},
    {"file": "gallery/backstage-2021.jpg",
     "caption": "Backstage перед панельной дискуссией.",
     "year": 2021, "tags": ["backstage"]},
    {"file": "gallery/organizers-2021.jpg",
     "caption": "Организаторы LUMEN FORUM.",
     "year": 2021, "tags": ["организаторы"]},

    # --- Сюжетные фото ---
    {"file": "gallery/photo-01-prime.jpg",
     "caption": "Команда PRIME SYSTEMS на LUMEN FORUM 2021.",
     "year": 2021, "tags": ["PRIME"], "story": "pavel+anna+maxim"},
    {"file": "gallery/photo-02-han-maxim.jpg",
     "caption": "Рабочая встреча на стенде партнёров.",
     "year": 2021, "tags": ["партнёры"], "story": "han+maxim"},
    {"file": "gallery/photo-03-belov-anna.jpg",
     "caption": "Обсуждение технической секции.",
     "year": 2021, "tags": ["секция"], "story": "belov+anna"},
    {"file": "gallery/photo-04-han-chong.jpg",
     "caption": "Участники дискуссии.",
     "year": 2021, "tags": ["дискуссия"], "story": "han+chong"},
    {"file": "gallery/photo-05-pavel-chong.jpg",
     "caption": "Во время кофе-брейка.",
     "year": 2021, "tags": ["кофе-брейк"], "story": "pavel+chong"},
    {
        "file": "gallery/photo-06-group.jpg",
        "caption": "Участники закрытой встречи LUMEN FORUM 2021.",
        "year": 2021,
        "tags": ["закрытая встреча"],
        "story": "pavel+anna+maxim+han+chong",
        "featured": True,
    },

    # --- Фото с номером 1704 ---
    {
        "file": "gallery/room-1704.jpg",
        "caption": "Конференц-зал во время подготовки.",
        "year": 2021,
        "tags": ["зал"],
        "clue": "Room 1704",
    },
]

# ------------------------------------------------------------------
# НОВОСТИ
# ------------------------------------------------------------------
NEWS = [
    {
        "slug": "lumen-2021-complete",
        "date": "20.04.2021",
        "title": "Завершился LUMEN FORUM 2021",
        "body": "Форум собрал рекордное число участников и партнёров.",
    },
    {
        "slug": "prime-new-partner",
        "date": "12.02.2019",
        "title": "PRIME SYSTEMS стал новым партнёром форума",
        "body": "Компания присоединилась к партнёрской программе LUMEN FORUM.",
    },
    {
        "slug": "han-joined-closed-section",
        "date": "14.04.2021",
        "title": "Хан Джэ Вон присоединился к закрытой секции",
        "body": "Хан Джэ Вон (Orbit Data) примет участие в закрытой технической секции форума.",
    },
    {
        "slug": "chong-special-panel",
        "date": "10.04.2021",
        "title": "Чон У Джин выступил в рамках специальной панели",
        "body": "Независимый консультант представил доклад «Закрытые коммуникационные системы».",
    },
    {
        "slug": "closed-meeting-2021",
        "date": "17.04.2021",
        "title": "Закрытая техническая секция",
        "body": (
            "В рамках закрытой технической секции состоялась встреча "
            "представителей PRIME SYSTEMS, Vector Labs и независимых "
            "технологических консультантов."
        ),
    },
    {
        "slug": "lumen-2026-announce",
        "date": "01.03.2026",
        "title": "Анонс LUMEN FORUM 2026",
        "body": "Форум 2026 года пройдёт осенью. Регистрация открыта.",
    },
]

# ------------------------------------------------------------------
# ПАРТНЁРЫ
# ------------------------------------------------------------------
PARTNERS = [
    {"key": "prime",  "name": "PRIME SYSTEMS",
     "desc": "Технологический партнёр, участник с 2019 года."},
    {"key": "vector", "name": "Vector Labs",
     "desc": "Исследовательский партнёр."},
    {"key": "orbit",  "name": "Orbit Data",
     "desc": "Партнёр в области аналитических решений."},
    {"key": "haeil",  "name": "Haeil & Partners",
     "desc": "Юридический партнёр форума."},
]