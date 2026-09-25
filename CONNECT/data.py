# -*- coding: utf-8 -*-

SITE = {
    "name": "CONNECT",
    "tagline": "Внутренняя платформа для юридических команд",
    "firm": "HAEIL & PARTNERS",
}

# Пароли. Публичный — обычный вход. Секретный — открывает скрытый слой.
PASSWORD_PUBLIC = "1234"
PASSWORD_SECRET = "1704"

# ------------------------------------------------------------------
# ПУБЛИЧНЫЕ ЧАТЫ (то, что видит любой юрист фирмы)
# ------------------------------------------------------------------
PUBLIC_CHATS = [
    {
        "id": "c1",
        "name": "Дело №112 — TechNova",
        "with": "Сергей Климов",
        "avatar": "СК",
        "color": "#2b6cb0",
        "unread": 0,
        "last": "Договор готов, отправил на согласование.",
        "messages": [
            {"from": "them", "time": "10:12",
             "text": "Добрый день. По делу TechNova нужен финальный вариант договора."},
            {"from": "me", "time": "10:15",
             "text": "Готовлю, отправлю до обеда."},
            {"from": "them", "time": "13:41",
             "text": "Спасибо, получил. Всё в порядке."},
            {"from": "me", "time": "13:43",
             "text": "Если будут правки — напишите."},
        ],
    },
    {
        "id": "c2",
        "name": "Корпоративный отдел",
        "with": "Ольга Миронова, Андрей Власов",
        "avatar": "КО",
        "color": "#805ad5",
        "unread": 2,
        "last": "Коллеги, напоминаю про встречу в пятницу.",
        "messages": [
            {"from": "them", "time": "09:14",
             "text": "Коллеги, напоминаю про встречу в пятницу в 15:00."},
            {"from": "them", "time": "09:15",
             "text": "Обсудим обновления по клиентам."},
            {"from": "me", "time": "09:20",
             "text": "Принято."},
        ],
    },
    {
        "id": "c3",
        "name": "IT-поддержка",
        "with": "Технический отдел",
        "avatar": "IT",
        "color": "#38a169",
        "unread": 0,
        "last": "Пароль обновлён, вход работает.",
        "messages": [
            {"from": "them", "time": "пн",
             "text": "Плановое обновление системы завершено."},
            {"from": "them", "time": "пн",
             "text": "Пароль обновлён, вход работает."},
        ],
    },
    {
        "id": "c4",
        "name": "Клиент: PRIME SYSTEMS",
        "with": "Максим Орлов",
        "avatar": "PS",
        "color": "#dd6b20",
        "unread": 0,
        "last": "Спасибо за оперативность.",
        "messages": [
            {"from": "them", "time": "вт",
             "text": "Нужна консультация по одному старому проекту."},
            {"from": "me", "time": "вт",
             "text": "Когда удобно обсудить?"},
            {"from": "them", "time": "вт",
             "text": "В четверг в 11:00."},
            {"from": "them", "time": "ср",
             "text": "Спасибо за оперативность."},
        ],
    },
    {
        "id": "c5",
        "name": "Личное",
        "with": "Е. Ким",
        "avatar": "ЕК",
        "color": "#d53f8c",
        "unread": 0,
        "last": "До встречи в Сеуле!",
        "messages": [
            {"from": "them", "time": "пт",
             "text": "Прилетаю в Сеул в среду."},
            {"from": "me", "time": "пт",
             "text": "Отлично! Обсудим по приезде."},
            {"from": "them", "time": "сб",
             "text": "До встречи в Сеуле!"},
        ],
    },
]

# ------------------------------------------------------------------
# СКРЫТЫЕ ЧАТЫ (то, что открывается по паролю 1704)
# ------------------------------------------------------------------
SECRET_CHATS = [
    {
        "id": "s1",
        "name": "USER-017",
        "with": "status: ACTIVE",
        "avatar": "17",
        "color": "#ff3344",
        "unread": 3,
        "last": "Last seen 21.09.2026 — 23:17",
        "messages": [
            {"from": "them", "time": "18.04.2019", "label": "archive",
             "text": "Account created by ADMIN-01."},
            {"from": "them", "time": "18.04.2019", "label": "archive",
             "text": "First login."},
            {"from": "me", "time": "17.04.2022", "label": "archive",
             "text": "Archive access requested."},
            {"from": "them", "time": "17.04.2025", "label": "archive",
             "text": "Login from unknown location."},
            {"from": "me", "time": "21.09.2026 23:17", "label": "live",
             "text": "Login successful.", "hot": True},
        ],
    },
    {
        "id": "s2",
        "name": "ADMIN-01",
        "with": "SYSTEM ADMINISTRATOR · REDACTED",
        "avatar": "A1",
        "color": "#ff3344",
        "unread": 1,
        "last": "21.09.2026 — 23:17",
        "messages": [
            {"from": "them", "time": "17.04.2019 18:41", "label": "archive",
             "text": "Account created at project transfer.", "hot": True},
            {"from": "them", "time": "18.04.2019 02:11", "label": "archive",
             "text": "Owner field REDACTED."},
            {"from": "me", "time": "21.06.2020 04:22", "label": "archive",
             "text": "File access: ADMIN_PROTOCOL.pdf"},
            {"from": "me", "time": "17.04.2022 00:00", "label": "archive",
             "text": "Archive access."},
            {"from": "them", "time": "21.09.2026 23:17", "label": "live",
             "text": "Login successful.", "hot": True},
        ],
    },
    {
        "id": "s3",
        "name": "C.U.",
        "with": "External Technical Consultant",
        "avatar": "CU",
        "color": "#ffcc33",
        "unread": 0,
        "last": "Access level: 5",
        "messages": [
            {"from": "them", "time": "17.04.2019", "label": "archive",
             "text": "Access level granted: LEVEL 5."},
            {"from": "them", "time": "17.04.2019", "label": "archive",
             "text": "Authorized: C-17, ADMIN, TRANSFER."},
            {"from": "me", "time": "17.04.2021", "label": "archive",
             "text": "Transfer completed."},
        ],
    },
    {
        "id": "s4",
        "name": "LEGACY MIGRATION",
        "with": "C17 → OD17",
        "avatar": "L",
        "color": "#00e5d0",
        "unread": 0,
        "last": "18.04.2019 — Migration supervisor: Y.B.",
        "messages": [
            {"from": "them", "time": "18.04.2019", "label": "archive",
             "text": "Users migrated: USER-002, USER-017, USER-021."},
            {"from": "them", "time": "18.04.2019", "label": "archive",
             "text": "Admin access migrated: ADMIN-01.", "hot": True},
            {"from": "them", "time": "18.04.2019", "label": "archive",
             "text": "Migration supervisor: Y.B."},
        ],
    },
    {
        "id": "s5",
        "name": "PRIVATE NODE 1704",
        "with": "STATUS: ONLINE",
        "avatar": "17",
        "color": "#ff3344",
        "unread": 0,
        "last": "Last connection: 21.09.2026 — 23:17",
        "messages": [
            {"from": "them", "time": "21.09.2026 23:17", "label": "live",
             "text": "ACTIVE SESSION.", "hot": True},
            {"from": "me", "time": "21.09.2026 23:19", "label": "live",
             "text": "USER-017 login confirmed."},
        ],
    },
]

# ------------------------------------------------------------------
# ПАНЕЛЬ УПРАВЛЕНИЯ (control.html)
# ------------------------------------------------------------------
CONTROL = {
    "title": "CONNECT // ROOT",
    "subtitle": "System administration panel",
    "stats": [
        {"label": "Active users", "value": "2"},
        {"label": "Sessions", "value": "1"},
        {"label": "Nodes online", "value": "1"},
        {"label": "Uptime", "value": "7y 4m"},
    ],
    "nodes": [
        {"id": "C-17", "status": "ARCHIVED", "location": "PRIME SYSTEMS"},
        {"id": "OD-17", "status": "ARCHIVED", "location": "ORBIT DATA / VECTOR LABS"},
        {"id": "CONNECT", "status": "ONLINE", "location": "UNKNOWN", "hot": True},
    ],
    "users": [
        {"id": "USER-017", "status": "ACTIVE", "last": "21.09.2026 23:17", "hot": True},
        {"id": "ADMIN-01", "status": "ACTIVE", "last": "21.09.2026 23:17", "hot": True},
        {"id": "USER-002", "status": "INACTIVE", "last": "2019"},
        {"id": "USER-021", "status": "INACTIVE", "last": "2021"},
    ],
    "log": [
        {"time": "17.04.2019 18:41", "text": "ADMIN-01 created", "hot": True},
        {"time": "18.04.2019 02:11", "text": "ADMIN-01 owner REDACTED"},
        {"time": "18.04.2019 02:13", "text": "USER-017 created"},
        {"time": "18.04.2019 03:14", "text": "C17 authentication accepted"},
        {"time": "17.04.2021 00:00", "text": "OD-17 transfer completed"},
        {"time": "17.04.2025 23:59", "text": "USER-017 login"},
        {"time": "21.09.2026 23:17", "text": "ADMIN-01 login successful", "hot": True},
        {"time": "21.09.2026 23:19", "text": "USER-017 login successful", "hot": True},
    ],
}