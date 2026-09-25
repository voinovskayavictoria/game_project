# -*- coding: utf-8 -*-

SITE = {
    "name": "VECTOR LABS",
    "tagline": "Engineering the invisible.",
    "founded": 2014,
    "description": (
        "Исследовательская технологическая компания, специализирующаяся "
        "на защищённых коммуникациях, аналитических системах и "
        "инфраструктуре данных."
    ),
}

EXTERNAL_LINKS = {
    "prime":  {"port": 5001, "name": "PRIME SYSTEMS"},
    "lumen":  {"port": 5002, "name": "LUMEN FORUM"},
    "haeil":  {"port": 5003, "name": "HAEIL & PARTNERS"},
    "orbit":  {"port": 5005, "name": "Orbit Data"},
    "c17arch":{"port": 5006, "name": "C-17 Archive"},
    "lebedeva":{"port": 5007, "name": "Мария Лебедева"},
}

HISTORY = [
    (2014, "Основание компании."),
    (2016, "Запуск исследовательского отдела."),
    (2018, "Расширение лаборатории."),
    (2019, "Новый технический центр."),
    (2021, "Международное сотрудничество."),
    (2024, "Запуск нового направления."),
]

# ------------------------------------------------------------------
# КОМАНДА
# ------------------------------------------------------------------
TEAM = [
    {
        "slug": "andrey-krylov",
        "name": "Андрей Крылов",
        "role": "CEO",
        "since": 2014,
        "photo": "img/team/krylov.jpg",
        "bio": "Соучредитель и генеральный директор VECTOR LABS.",
        "featured": True,
    },
    {
        "slug": "viktoria-orlova",
        "name": "Виктория Орлова",
        "role": "CTO",
        "since": 2014,
        "photo": "img/team/orlova.jpg",
        "bio": "Технический директор. Отвечает за исследовательское направление.",
        "featured": True,
    },
    {
        "slug": "mikhail-gromov",
        "name": "Михаил Громов",
        "role": "Security Engineer",
        "since": 2017,
        "photo": "img/team/gromov.jpg",
        "bio": "Специалист по безопасности распределённых систем.",
        "featured": True,
    },
    {
        "slug": "elena-kotova",
        "name": "Елена Котова",
        "role": "Product Manager",
        "since": 2018,
        "photo": "img/team/kotova.jpg",
        "bio": "Продуктовый менеджер исследовательских проектов.",
        "featured": False,
    },
    {
        "slug": "ilya-romanov",
        "name": "Илья Романов",
        "role": "Software Engineer",
        "since": 2020,
        "photo": "img/team/romanov.jpg",
        "bio": "Разработчик внутренних систем.",
        "featured": False,
    },
    {
        "slug": "yuri-belov",
        "name": "Юрий Белов",
        "role": "Senior Systems Engineer",
        "since": 2019,
        "photo": "img/team/belov.jpg",
        "featured": True,
        "bio": (
            "Специалист по распределённым системам и защищённым "
            "коммуникациям."
        ),
        "career": [
            "2013–2017 — Digital Core",
            "2017–2019 — PRIME SYSTEMS",
            "2019–н.в. — VECTOR LABS",
        ],
        "specialization": [
            "backend systems",
            "authentication",
            "secure communication",
            "legacy infrastructure",
        ],
        "selected_projects": ["OD-17", "Legacy Communications"],
        "clue": "Присоединился к VECTOR LABS в апреле 2019 года — в том же месяце, когда C-17 был передан внешней команде.",
    },
    # ещё немного обычных сотрудников
    {"slug": "anton-belov", "name": "Антон Белов", "role": "QA Engineer",
     "since": 2020, "photo": "img/team/belov_a.jpg",
     "bio": "Тестирование внутренних сервисов.", "featured": False},
    {"slug": "daria-novikova", "name": "Дарья Новикова", "role": "Data Analyst",
     "since": 2021, "photo": "img/team/novikova.jpg",
     "bio": "Аналитика исследовательских данных.", "featured": False},
]

# ------------------------------------------------------------------
# ПРОЕКТЫ
# ------------------------------------------------------------------
PROJECTS = [
    {"slug": "vector-cloud", "title": "Vector Cloud", "status": "active",
     "period": "2021–н.в.", "summary": "Облачная платформа для исследовательских команд."},
    {"slug": "v-secure", "title": "V-Secure", "status": "active",
     "period": "2022–н.в.", "summary": "Фреймворк для защищённого обмена данными."},
    {"slug": "helix", "title": "Helix", "status": "active",
     "period": "2024–н.в.", "summary": "Исследовательский проект по распределённым графам."},
    {"slug": "od17", "title": "OD-17", "status": "archived",
     "period": "2019–2021", "summary": "Экспериментальная система защищённой коммуникации для ограниченного круга пользователей.",
     "lead": "Юрий Белов", "featured": True},
    {"slug": "legacy-communications", "title": "Legacy Communications", "status": "archived",
     "period": "2019–2020", "summary": "Поддержка и миграция устаревших коммуникационных систем."},
    {"slug": "atlas-v", "title": "Atlas", "status": "archived",
     "period": "2017–2019", "summary": "Внутренняя система управления данными."},
    {"slug": "orion-v", "title": "Orion", "status": "archived",
     "period": "2016–2018", "summary": "Первая исследовательская платформа компании."},
]

# ------------------------------------------------------------------
# OD-17 — детали
# ------------------------------------------------------------------
OD17 = {
    "title": "OD-17",
    "status": "Archived",
    "period": "2019–2021",
    "lead": "Юрий Белов",
    "description": (
        "Экспериментальная система защищённой коммуникации "
        "для ограниченного круга пользователей."
    ),
    "team": [
        {"name": "Юрий Белов", "role": "Lead Engineer", "external": None},
        {"name": "Михаил Громов", "role": "Security", "external": None},
        {"name": "Хан Джэ Вон", "role": "External Consultant", "external": "orbit"},
    ],
    "documents": [
        {"id": "OD17_2019", "name": "OD17_2019.pdf",
         "date": "2019", "note": "Начало проекта."},
        {"id": "OD17_2020", "name": "OD17_2020.pdf",
         "date": "2020", "note": "Обновление системы."},
        {"id": "OD17_2021", "name": "OD17_2021.pdf",
         "date": "2021", "note": "Проект переведён в архив."},
        {"id": "OD17_LEGACY", "name": "OD17_LEGACY_REF.pdf",
         "date": "2019", "note": "Ссылка на устаревшую инфраструктуру.",
         "clue": "Legacy reference: C17"},
    ],
}

# ------------------------------------------------------------------
# SYSTEM LOG
# ------------------------------------------------------------------
SYSTEM_LOG = [
    {"date": "17.04.2019", "time": "19:02", "text": "Legacy connection established", "hot": True},
    {"date": "18.04.2019", "time": "03:14", "text": "C17 authentication accepted", "hot": True},
    {"date": "21.04.2019", "time": "11:47", "text": "USER-017 migrated"},
    {"date": "22.04.2019", "time": "09:32", "text": "OD-17 first build"},
    {"date": "12.08.2020", "time": "15:08", "text": "External consultants joined OD-17"},
    {"date": "03.02.2021", "time": "17:00", "text": "OD-17 archived"},
]

# ------------------------------------------------------------------
# НОВОСТИ
# ------------------------------------------------------------------
NEWS = [
    {"slug": "new-research-direction",
     "date": "19.04.2019",
     "title": "VECTOR LABS объявила о запуске нового исследовательского направления",
     "body": "Компания расширяет исследовательскую программу."},
    {"slug": "yuri-belov-joins",
     "date": "23.04.2019",
     "title": "В компанию присоединился инженер Юрий Белов",
     "body": "Юрий Белов усилил команду исследовательского отдела."},
    {"slug": "external-consultants",
     "date": "12.08.2020",
     "title": "VECTOR LABS заключила соглашение с внешними технологическими консультантами",
     "body": "Компания расширяет пул внешних экспертов."},
    {"slug": "od17-archived",
     "date": "03.02.2021",
     "title": "Проект OD-17 переведён в архив",
     "body": "Работы по проекту OD-17 завершены, материалы переданы в архив."},
    {"slug": "new-direction-2024",
     "date": "10.03.2024",
     "title": "Запуск нового направления — распределённые графы",
     "body": "VECTOR LABS начинает новую исследовательскую программу."},
]

# ------------------------------------------------------------------
# ГАЛЕРЕЯ
# ------------------------------------------------------------------
GALLERY = [
    {"file": "gallery/office-1.jpg", "caption": "Главный офис VECTOR LABS.", "year": 2022},
    {"file": "gallery/office-2.jpg", "caption": "Лаборатория.", "year": 2022},
    {"file": "gallery/team-2021.jpg", "caption": "Команда исследовательского отдела.", "year": 2021},
    {
        "file": "gallery/od17-2019.jpg",
        "caption": "Команда исследовательского отдела после завершения первого этапа OD-17.",
        "year": 2019,
        "story": "belov+han",
    },
    {
        "file": "gallery/consultants-2020.jpg",
        "caption": "Встреча с внешними техническими консультантами.",
        "year": 2020,
        "story": "han+chong",
    },
    {"file": "gallery/conference-2022.jpg", "caption": "Отраслевая конференция.", "year": 2022},
]

# ------------------------------------------------------------------
# ПАРТНЁРЫ
# ------------------------------------------------------------------
PARTNERS = ["prime", "orbit", "lumen", "haeil"]

# ------------------------------------------------------------------
# LEGACY MIGRATION DOCUMENT
# ------------------------------------------------------------------
LEGACY_MIGRATION = {
    "title": "LEGACY C17 → OD17 MIGRATION",
    "date": "18.04.2019",
    "summary": "Перенос пользовательской базы и отдельных компонентов старой системы.",
    "users_migrated": ["USER-002", "USER-017", "USER-021"],
    "admin_migrated": "ADMIN-01",
    "supervisor": "Y.B.",
}