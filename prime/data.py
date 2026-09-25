# -*- coding: utf-8 -*-

SITE = {
    "name": "PRIME SYSTEMS",
    "tagline": "Технологии, которые соединяют людей.",
    "founded": 2009,
}

# ------------------------------------------------------------------
# КОМАНДА
# ------------------------------------------------------------------
TEAM = [
    # --- Трое ключевых ---
    {
        "slug": "pavel-sokolov",
        "name": "Павел Соколов",
        "role": "CEO / генеральный директор",
        "age": 41,
        "since": 2015,
        "photo": "img/team/sokolov.jpg",
        "featured": True,
        "short": "Отвечает за стратегию компании. Публичный представитель PRIME.",
        "bio": (
            "Павел присоединился к PRIME SYSTEMS в 2015 году. "
            "Под его руководством компания расширила направление "
            "корпоративных IT-решений и вышла на международный рынок."
        ),
        "education": [
            "Московский технический университет",
            "Факультет вычислительной техники",
            "2003–2008",
        ],
        "career": [
            "2008–2012 — TechNova",
            "2012–2015 — Vector Systems",
            "2015–н.в. — PRIME SYSTEMS",
        ],
        "extra_links": [
            {"label": "Lumen Forum →", "url": "http://localhost:5002/"},
        ],
    },
    {
        "slug": "anna-voronova",
        "name": "Анна Воронова",
        "role": "CTO / технический директор",
        "age": 36,
        "since": 2017,
        "photo": "img/team/voronova.jpg",
        "featured": True,
        "short": "Руководит техническим отделом. Специализация — информационные системы.",
        "bio": (
            "Анна руководит разработкой и инфраструктурой PRIME SYSTEMS. "
            "Курировала разработку ядра корпоративной платформы и "
            "передачу проекта C-17 внешней команде."
        ),
        "education": [
            "Санкт-Петербургский политехнический университет",
            "Факультет информационных систем",
            "2006–2011",
        ],
        "career": [
            "2011–2014 — Digital Core",
            "2014–2017 — Vector Systems",
            "2017–н.в. — PRIME SYSTEMS",
        ],
        "projects": [
            {
                "title": "C-17 — экспериментальная коммуникационная архитектура",
                "period": "2018–2019",
                "status": "архивный",
                "link": "/projects/c17",
            },
        ],
    },
    {
        "slug": "maxim-orlov",
        "name": "Максим Орлов",
        "role": "COO / операционный директор",
        "age": 39,
        "since": 2018,
        "photo": "img/team/orlov.jpg",
        "featured": True,
        "short": "Отвечает за партнёрские отношения и внутренние процессы.",
        "bio": (
            "Отвечает за партнёрские отношения, внутренние процессы "
            "и взаимодействие с внешними организациями."
        ),
        "career": [
            "2008–2014 — Orion Logistics",
            "2014–2018 — Independent Consultant",
            "2018–н.в. — PRIME SYSTEMS",
        ],
        "partner_links": [
            {"label": "Lumen Forum", "url": "http://localhost:5002/"},
            {"label": "Haeil & Partners", "url": "http://localhost:5003/"},
            {"label": "Orbit Data", "url": "http://localhost:5005/"},
            {"label": "Vector Labs", "url": "http://localhost:5004/"},
        ],
    },

    # --- Обычные сотрудники (чтобы сайт выглядел живым) ---
    {"slug": "dmitry-krylov", "name": "Дмитрий Крылов", "role": "PR-директор",
     "age": 38, "since": 2019, "photo": "img/team/krylov.jpg", "featured": False,
     "short": "Отвечает за коммуникации и публичные мероприятия."},
    {"slug": "elena-morozova", "name": "Елена Морозова", "role": "HR-директор",
     "age": 42, "since": 2016, "photo": "img/team/morozova.jpg", "featured": False,
     "short": "Подбор, адаптация и развитие сотрудников."},
    {"slug": "alexey-fedorov", "name": "Алексей Фёдоров", "role": "Senior Developer",
     "age": 34, "since": 2018, "photo": "img/team/fedorov.jpg", "featured": False,
     "short": "Разработка корпоративных сервисов."},
    {"slug": "marina-sokolova", "name": "Марина Соколова", "role": "Финансовый директор",
     "age": 45, "since": 2014, "photo": "img/team/sokolova_m.jpg", "featured": False,
     "short": "Финансовое планирование и отчётность."},
    {"slug": "sergey-nikitin", "name": "Сергей Никитин", "role": "Project Manager",
     "age": 37, "since": 2019, "photo": "img/team/nikitin.jpg", "featured": False,
     "short": "Ведёт ключевые клиентские проекты."},
    {"slug": "irina-volkova", "name": "Ирина Волкова", "role": "QA Lead",
     "age": 33, "since": 2018, "photo": "img/team/volkova.jpg", "featured": False,
     "short": "Контроль качества и тестирование."},
    {"slug": "nikita-solovyev", "name": "Никита Соловьёв", "role": "DevOps Engineer",
     "age": 31, "since": 2020, "photo": "img/team/solovyev.jpg", "featured": False,
     "short": "Инфраструктура, CI/CD, мониторинг."},
    {"slug": "olga-kuznetsova", "name": "Ольга Кузнецова", "role": "Директор по маркетингу",
     "age": 36, "since": 2017, "photo": "img/team/kuznetsova.jpg", "featured": False,
     "short": "Маркетинг и продвижение продуктов."},
    {"slug": "artem-smirnov", "name": "Артём Смирнов", "role": "Backend Developer",
     "age": 29, "since": 2021, "photo": "img/team/smirnov.jpg", "featured": False,
     "short": "Серверная разработка."},
    {"slug": "tatyana-pavlova", "name": "Татьяна Павлова", "role": "Аналитик",
     "age": 30, "since": 2020, "photo": "img/team/pavlova.jpg", "featured": False,
     "short": "Бизнес-анализ и отчётность."},
    {"slug": "roman-egorov", "name": "Роман Егоров", "role": "Системный администратор",
     "age": 35, "since": 2016, "photo": "img/team/egorov.jpg", "featured": False,
     "short": "Внутренняя инфраструктура."},
    {"slug": "viktoria-romanova", "name": "Виктория Романова", "role": "Дизайнер",
     "age": 28, "since": 2021, "photo": "img/team/romanova.jpg", "featured": False,
     "short": "UX/UI корпоративных продуктов."},
]

# ------------------------------------------------------------------
# ПРОЕКТЫ
# ------------------------------------------------------------------
PROJECTS = [
    {
        "slug": "prime-cloud", "title": "PRIME Cloud",
        "status": "active", "period": "2021–н.в.",
        "short": "Облачная платформа для корпоративных заказчиков.",
    },
    {
        "slug": "prime-secure", "title": "PRIME Secure",
        "status": "active", "period": "2022–н.в.",
        "short": "Решения для защищённого обмена данными.",
    },
    {
        "slug": "connect-business", "title": "Connect Business",
        "status": "active", "period": "2023–н.в.",
        "short": "Корпоративный мессенджер для среднего бизнеса.",
    },
    {
        "slug": "prime-analytics", "title": "Prime Analytics",
        "status": "active", "period": "2024–н.в.",
        "short": "Аналитическая платформа для принятия решений.",
    },
    {
        "slug": "c17",
        "title": "C-17",
        "status": "archived",
        "period": "2018–2019",
        "short": "Экспериментальная система корпоративной коммуникации.",
        "archived": True,
        "team": [
            "Анна Воронова — Technical Lead",
            "Юрий Белов — Software Engineer",
            "Чон У Джин — External Consultant",
        ],
        "description": (
            "Проект был создан как экспериментальная система защищённого "
            "обмена информацией между пользователями."
        ),
        "last_note": "17.04.2019 — проект передан внешней команде.",
        "meta": {
            "project_id": "C17",
            "archive_ref": "1704",
            "transfer_date": "17/04/2019",
        },
    },
    {"slug": "atlas", "title": "Project Atlas", "status": "archived",
     "period": "2016–2017", "short": "Внутренняя система документооборота."},
    {"slug": "mercury", "title": "Mercury", "status": "archived",
     "period": "2015–2016", "short": "Платёжный шлюз для партнёров."},
    {"slug": "orion", "title": "Orion", "status": "archived",
     "period": "2013–2014", "short": "Первая корпоративная CRM компании."},
]

# ------------------------------------------------------------------
# НОВОСТИ
# ------------------------------------------------------------------
NEWS = [
    {"slug": "agreement-2026", "date": "12.09.2026",
     "title": "PRIME SYSTEMS заключила новое соглашение о технологическом сотрудничестве",
     "body": "Компания продолжает расширять партнёрскую сеть."},
    {"slug": "sokolov-forum-2026", "date": "04.09.2026",
     "title": "Павел Соколов выступил на технологическом форуме",
     "body": "CEO PRIME SYSTEMS представил стратегию компании на ближайшие годы."},
    {"slug": "platform-2026", "date": "27.08.2026",
     "title": "Компания представила обновлённую корпоративную платформу",
     "body": "Новая версия PRIME Cloud доступна партнёрам."},
    {"slug": "anniversary-2026", "date": "18.08.2026",
     "title": "PRIME SYSTEMS отмечает очередную годовщину",
     "body": "Компания работает на рынке уже более пятнадцати лет."},

    {"slug": "new-office-2025", "date": "03.11.2025",
     "title": "Открыт новый офис в деловом центре",
     "body": "Компания расширяет присутствие."},
    {"slug": "conference-2024", "date": "22.05.2024",
     "title": "PRIME SYSTEMS приняла участие в отраслевой конференции",
     "body": "Команда представила решения для корпоративного сектора."},
    {"slug": "product-2024", "date": "14.02.2024",
     "title": "Выпущен новый продукт Prime Analytics",
     "body": "Платформа для анализа корпоративных данных."},
    {"slug": "restructure-2021", "date": "06.09.2021",
     "title": "Изменения в структуре компании",
     "body": "PRIME SYSTEMS объявляет о реорганизации подразделений."},
    {"slug": "c17-internal-complete-2019", "date": "17.04.2019",
     "title": "PRIME SYSTEMS завершила внутренний этап проекта C-17",
     "body": (
         "После завершения внутреннего этапа дальнейшее развитие проекта "
         "было передано внешней команде."
     )},
]

# ------------------------------------------------------------------
# ПАРТНЁРЫ
# ------------------------------------------------------------------
PARTNERS = [
    {"name": "Lumen Forum", "desc": "Технологическая конференция.",
     "url": "http://localhost:5002/"},
    {"name": "Haeil & Partners", "desc": "Юридическое сопровождение.",
     "url": "http://localhost:5003/"},
    {"name": "Vector Labs", "desc": "Технологический партнёр.",
     "url": "http://localhost:5004/"},
    {"name": "Orbit Data", "desc": "Аналитические решения.",
     "url": "http://localhost:5005/"},
]