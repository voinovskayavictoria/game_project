# -*- coding: utf-8 -*-

SITE = {
    "name": "ORBIT DATA",
    "tagline": "Data beyond boundaries.",
    "founded": 2016,
    "description": (
        "Компания, специализирующаяся на обработке данных, аналитических "
        "системах и инфраструктуре защищённых цифровых сервисов."
    ),
}

EXTERNAL_LINKS = {
    "prime":  {"port": 5001, "name": "PRIME SYSTEMS"},
    "lumen":  {"port": 5002, "name": "LUMEN FORUM"},
    "haeil":  {"port": 5003, "name": "HAEIL & PARTNERS"},
    "vector": {"port": 5004, "name": "Vector Labs"},
    "c17arch":{"port": 5006, "name": "C-17 Archive"},
    "lebedeva":{"port": 5007, "name": "Мария Лебедева"},
    "cacao":  {"port": 5008, "name": "Чёрный какао"},
}

HISTORY = [
    (2016, "Основание компании."),
    (2018, "Запуск аналитического подразделения."),
    (2019, "Расширение инфраструктуры."),
    (2020, "Создание исследовательского отдела."),
    (2021, "Запуск проекта OD-17."),
    (2023, "Международное развитие."),
]

# ------------------------------------------------------------------
# КОМАНДА
# ------------------------------------------------------------------
TEAM = [
    {"slug": "alexey-melnikov", "name": "Алексей Мельников", "role": "CEO",
     "since": 2016, "photo": "img/team/melnikov.jpg", "featured": True,
     "bio": "Соучредитель и генеральный директор ORBIT DATA."},
    {"slug": "marina-vlasova", "name": "Марина Власова", "role": "CTO",
     "since": 2016, "photo": "img/team/vlasova.jpg", "featured": True,
     "bio": "Технический директор. Отвечает за инфраструктуру и продукты."},
    {"slug": "denis-korolev", "name": "Денис Королев", "role": "Security Engineer",
     "since": 2018, "photo": "img/team/korolev.jpg", "featured": True,
     "bio": "Специалист по безопасности."},
    {
        "slug": "han-jae-won",
        "name": "Хан Джэ Вон",
        "role": "Director of Research",
        "since": 2021,
        "photo": "img/team/han.jpg",
        "featured": True,
        "bio": (
            "Руководитель исследовательского направления. "
            "Отвечает за проекты в области защищённых систем и "
            "инфраструктуры идентификации."
        ),
        "career": [
            "2014–2018 — Digital Core",
            "2018–2021 — независимый консультант",
            "2021–н.в. — ORBIT DATA",
        ],
        "specialization": [
            "data infrastructure",
            "secure systems",
            "distributed architecture",
            "identity systems",
        ],
        "selected_projects": ["OD-17", "Secure Identity"],
        "social": {
            "linkedin": "https://linkedin.com/in/hanjw",
            "instagram": "/team/han-jae-won/instagram",
            "telegram": "/team/han-jae-won/telegram",
        },
        "clue": (
            "Ранее сотрудничал с VECTOR LABS как внешний консультант по "
            "проекту OD-17."
        ),
    },
    {"slug": "olga-lebedeva", "name": "Ольга Лебедева", "role": "Data Scientist",
     "since": 2019, "photo": "img/team/lebedeva_o.jpg", "featured": False,
     "bio": "Исследования и моделирование данных."},
    {"slug": "pavel-orlov", "name": "Павел Орлов", "role": "Backend Engineer",
     "since": 2020, "photo": "img/team/orlov_p.jpg", "featured": False,
     "bio": "Серверная разработка."},
]

# ------------------------------------------------------------------
# ПРОЕКТЫ
# ------------------------------------------------------------------
PROJECTS = [
    {"slug": "orbit-cloud", "title": "ORBIT Cloud", "status": "active",
     "period": "2021–н.в.", "summary": "Облачная аналитическая платформа."},
    {"slug": "datasphere", "title": "DataSphere", "status": "active",
     "period": "2022–н.в.", "summary": "Распределённое хранилище данных."},
    {"slug": "od-analytics", "title": "OD Analytics", "status": "active",
     "period": "2023–н.в.", "summary": "Инструменты аналитики для корпоративных клиентов."},
    {"slug": "secure-identity", "title": "Secure Identity", "status": "active",
     "period": "2024–н.в.", "summary": "Система идентификации пользователей."},
    {"slug": "helix-o", "title": "Helix", "status": "archived",
     "period": "2020–2022", "summary": "Исследовательский проект по графам данных."},
    {"slug": "atlas-o", "title": "Atlas", "status": "archived",
     "period": "2018–2020", "summary": "Внутренняя система управления."},
    {
        "slug": "od17",
        "title": "OD-17",
        "status": "archived",
        "period": "2019–2021",
        "summary": "Исследовательский проект по созданию защищённой системы коммуникации и идентификации пользователей.",
        "lead": "H. J. Won",
        "technical_partner": "VECTOR LABS",
        "featured": True,
    },
]

# ------------------------------------------------------------------
# OD-17 — детали
# ------------------------------------------------------------------
OD17 = {
    "title": "OD-17",
    "status": "Archived",
    "lead": "H. J. Won",
    "technical_partner": "VECTOR LABS",
    "start": 2019,
    "end": 2021,
    "description": (
        "Исследовательский проект по созданию защищённой системы "
        "коммуникации и идентификации пользователей."
    ),
    "documents": [
        {"id": "OD17_REPORT_2019", "name": "OD17_REPORT_2019.pdf",
         "date": "2019", "note": "Отчёт за первый год. Технический партнёр — VECTOR LABS."},
        {"id": "OD17_REPORT_2020", "name": "OD17_REPORT_2020.pdf",
         "date": "2020", "note": "Упоминается перенос старой инфраструктуры."},
        {"id": "OD17_FINAL", "name": "OD17_FINAL.pdf",
         "date": "17.04.2021",
         "note": "Финальный отчёт.",
         "clue": "Legacy system remains operational."},
        {"id": "OD17_TRANSFER_2021", "name": "OD17_TRANSFER_2021.pdf",
         "date": "17.04.2021",
         "note": "Документ о передаче проекта.",
         "special": "transfer"},
    ],
    "users": [
        {"id": "USER-002", "status": "INACTIVE", "last": "2019"},
        {"id": "USER-017", "status": "ACTIVE", "last": "21.09.2026"},
        {"id": "USER-021", "status": "INACTIVE", "last": "2021"},
        {"id": "USER-034", "status": "INACTIVE", "last": "2020"},
        {"id": "USER-041", "status": "INACTIVE", "last": "2020"},
    ],
    "access_control": [
        {"id": "ADMIN-01", "role": "SYSTEM ADMINISTRATOR", "status": "ACTIVE",
         "note": "ADMIN-01 migrated from C-17"},
        {"id": "ADMIN-02", "role": "ORBIT ADMIN", "status": "INACTIVE"},
    ],
}

# ------------------------------------------------------------------
# TRANSFER DOCUMENT (2021)
# ------------------------------------------------------------------
TRANSFER_2021 = {
    "title": "OD17_TRANSFER_2021.pdf",
    "date": "17.04.2021",
    "project": "OD-17",
    "previous_infra": "C-17",
    "administrator": "ADMIN-01",
    "technical_consultant": "C.U.",
    "research_director": "H. J. Won",
}

CONSULTANT = {
    "code": "C.U.",
    "role": "External Technical Consultant",
    "full_name": "Чон У Джин",
    "access_level": 5,
    "authorized": ["C-17", "OD-17", "TRANSFER"],
    "note": (
        "Профиль восстановлен из архивной системы. "
        "Используется как внешний технический консультант "
        "в нескольких связанных проектах."
    ),
}

# ------------------------------------------------------------------
# СОЦИАЛЬНЫЕ СТРАНИЦЫ ХАНА (игровые)
# ------------------------------------------------------------------
HAN_INSTAGRAM = {
    "handle": "@h.j.won",
    "posts": [
        {
            "date": "16.09.2026",
            "image": "img/social/han-1609.jpg",
            "caption": "Хорошее место для работы. И для тишины.",
            "location": "Где-то в центре",
            "photo_hint": (
                "На заднем плане — знакомый интерьер. "
                "Столик у окна, деревянные панели, "
                "вывеска соседнего магазина."
            ),
        },
        {
            "date": "02.09.2026",
            "image": "img/social/han-0209.jpg",
            "caption": "Обычное утро.",
        },
    ],
}

HAN_TELEGRAM = {
    "handle": "@hjwon",
    "messages": [
        {"date": "18.09.2026", "time": "22:41", "text": "Здесь хорошо."},
        {"date": "19.09.2026", "time": "23:12", "text": "Приду ещё."},
        {"date": "20.09.2026", "time": "23:59", "text": "Завтра снова туда.", "hot": True},
    ],
}

# ------------------------------------------------------------------
# ГАЛЕРЕЯ
# ------------------------------------------------------------------
GALLERY = [
    {"file": "gallery/office-1.jpg", "caption": "Головной офис ORBIT DATA.", "year": 2022},
    {"file": "gallery/office-2.jpg", "caption": "Аналитический отдел.", "year": 2023},
    {
        "file": "gallery/2019-belov-han.jpg",
        "caption": "Совместная работа с техническим партнёром.",
        "year": 2019,
        "story": "belov+han",
    },
    {"file": "gallery/2020-team.jpg", "caption": "Исследовательская команда.", "year": 2020},
    {
        "file": "gallery/2021-han-chong.jpg",
        "caption": "Закрытая встреча исследовательского отдела.",
        "year": 2021,
        "story": "han+chong",
    },
]

# ------------------------------------------------------------------
# НОВОСТИ
# ------------------------------------------------------------------
NEWS = [
    {"slug": "external-consultants-2019", "date": "18.04.2019",
     "title": "ORBIT DATA начинает сотрудничество с внешними технологическими консультантами",
     "body": "Компания расширяет экспертизу в области защищённых систем."},
    {"slug": "identity-2020", "date": "12.08.2020",
     "title": "Исследовательская группа расширяет работу над системами идентификации",
     "body": "Направление систем идентификации становится одним из ключевых."},
    {"slug": "od17-archived-2021", "date": "17.04.2021",
     "title": "Проект OD-17 переведён в архив",
     "body": "Работы по проекту OD-17 официально завершены."},
    {"slug": "od17-support-2022", "date": "10.03.2022",
     "title": "ORBIT DATA прекращает публичную поддержку OD-17",
     "body": "Все материалы проекта переведены в закрытый архив."},
    {"slug": "international-2023", "date": "22.05.2023",
     "title": "Международное развитие ORBIT DATA",
     "body": "Компания открывает представительства в двух странах."},
]

# ------------------------------------------------------------------
# ПАРТНЁРЫ
# ------------------------------------------------------------------
PARTNERS = ["prime", "vector", "lumen", "haeil"]