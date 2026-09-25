# -*- coding: utf-8 -*-

SITE = {
    "name": "C-17 // ARCHIVE",
    "status": "ARCHIVED",
    "last_public_update": "17.04.2019",
}

EXTERNAL_LINKS = {
    "prime":  {"port": 5001, "name": "PRIME SYSTEMS"},
    "lumen":  {"port": 5002, "name": "LUMEN FORUM"},
    "haeil":  {"port": 5003, "name": "HAEIL & PARTNERS"},
    "vector": {"port": 5004, "name": "Vector Labs"},
    "orbit":  {"port": 5005, "name": "Orbit Data"},
}

PROJECT = {
    "id": "C17",
    "created": 2018,
    "status": "ARCHIVED",
    "owner": "PRIME SYSTEMS",
    "tech_lead": "A. VORONOVA",
    "description": "Experimental secure communication architecture.",
    "transfer_date": "17.04.2019",
    "external_consultant": "C.U.",
}

USERS = [
    {"id": "USER-001", "name": "A.VORONOVA", "status": "DEACTIVATED",
     "since": "2018", "last": "2019", "role": "TECHNICAL LEAD"},
    {"id": "USER-002", "name": "Y.BELOV", "status": "DEACTIVATED",
     "since": "2018", "last": "2019", "role": "SOFTWARE ENGINEER"},
    {"id": "USER-003", "name": "P.SOKOLOV", "status": "DEACTIVATED",
     "since": "2018", "last": "2019", "role": "EXECUTIVE"},
    {"id": "USER-004", "name": "M.ORLOV", "status": "DEACTIVATED",
     "since": "2018", "last": "2019", "role": "OPERATIONS"},
    {
        "id": "USER-017",
        "name": "UNKNOWN",
        "status": "ACTIVE",
        "since": "18.04.2019",
        "last": "21.09.2026 — 23:17",
        "role": "UNDEFINED",
        "note": "Account created by ADMIN-01. Name not set.",
    },
    {"id": "USER-021", "name": "H.J.WON", "status": "DEACTIVATED",
     "since": "2019", "last": "2021", "role": "EXTERNAL"},
    {
        "id": "ADMIN-01",
        "name": "REDACTED",
        "status": "ACTIVE",
        "since": "17.04.2019",
        "last": "21.09.2026",
        "role": "SYSTEM ADMINISTRATOR",
        "note": "Owner name redacted at 18.04.2019 02:11.",
    },
]

ACCESS_LOG = [
    {"date": "17.04.2019", "time": "18:41", "user": "ADMIN-01", "action": "PROJECT TRANSFER", "location": "1704"},
    {"date": "18.04.2019", "time": "02:17", "user": "USER-017", "action": "LOGIN", "location": "UNKNOWN"},
    {"date": "21.06.2020", "time": "04:22", "user": "ADMIN-01", "action": "FILE ACCESS", "location": "UNKNOWN"},
    {"date": "04.11.2021", "time": "22:08", "user": "USER-017", "action": "LOGIN", "location": "UNKNOWN"},
    {"date": "17.04.2022", "time": "00:00", "user": "ADMIN-01", "action": "ARCHIVE ACCESS", "location": "UNKNOWN"},
    {"date": "17.04.2025", "time": "23:59", "user": "USER-017", "action": "LOGIN", "location": "UNKNOWN"},
    {"date": "21.09.2026", "time": "23:17", "user": "ADMIN-01", "action": "LOGIN", "location": "UNKNOWN"},
    {"date": "21.09.2026", "time": "23:19", "user": "USER-017", "action": "LOGIN", "location": "UNKNOWN"},
]

CHANGELOG = [
    {"date": "2018", "text": "C-17 initialized"},
    {"date": "2019", "text": "Security architecture update"},
    {"date": "17.04.2019", "text": "PROJECT TRANSFER", "hot": True},
    {"date": "18.04.2019", "text": "Administrative access modified"},
    {"date": "2020", "text": "External maintenance"},
    {"date": "2021", "text": "Authentication update"},
    {"date": "2022", "text": "Archive migration"},
    {"date": "2025", "text": "Legacy access restored"},
    {"date": "2026", "text": "System activity detected", "hot": True},
]

FILES = [
    {"id": "C17_ARCHITECTURE", "name": "C17_ARCHITECTURE.pdf",
     "status": "ok", "size": "1.2 MB", "modified": "2019-03-11",
     "content": (
         "Общая архитектура системы C-17. Три уровня доступа. "
         "Изолированный контур. Спецификация внешнего API — отсутствует."
     )},
    {"id": "TRANSFER_1704", "name": "TRANSFER_1704.pdf",
     "status": "ok", "size": "340 KB", "modified": "2019-04-17",
     "content": "PROJECT TRANSFER RECORD", "special": "transfer"},
    {"id": "USERS", "name": "USERS.csv",
     "status": "ok", "size": "4 KB", "modified": "2019-04-18",
     "content": (
         "USER-001,A.VORONOVA,DEACTIVATED\n"
         "USER-002,Y.BELOV,DEACTIVATED\n"
         "USER-003,P.SOKOLOV,DEACTIVATED\n"
         "USER-004,M.ORLOV,DEACTIVATED\n"
         "USER-017,UNKNOWN,ACTIVE\n"
         "USER-021,H.J.WON,DEACTIVATED\n"
         "ADMIN-01,REDACTED,ACTIVE"
     )},
    {"id": "ACCESS_LOG", "name": "ACCESS_LOG.txt",
     "status": "ok", "size": "12 KB", "modified": "2026-09-21",
     "content": "See /access-log for parsed view."},
    {"id": "ADMIN_PROTOCOL", "name": "ADMIN_PROTOCOL.pdf",
     "status": "corrupted", "size": "???", "modified": "2019-04-18",
     "content": "FILE CORRUPTED"},
    {"id": "PROJECT_NOTES", "name": "PROJECT_NOTES.txt",
     "status": "ok", "size": "3 KB", "modified": "2019-04-16",
     "content": (
         "Заметки по проекту. Внешний консультант — C.U. "
         "Уровень доступа: 5. Подпись: /archive/c17/1704"
     ), "special": "notes"},
    {"id": "MIGRATION_2022", "name": "MIGRATION_2022.pdf",
     "status": "denied", "size": "—", "modified": "2022",
     "content": "ACCESS DENIED"},
    {"id": "CU_PROFILE", "name": "C.U.",
     "status": "ok", "size": "1 KB", "modified": "2019-04-17",
     "content": "external consultant profile", "special": "cu"},
    {"id": "PHOTO_1704", "name": "1704.jpg",
     "status": "ok", "size": "820 KB", "modified": "2019-04-15",
     "content": "photo", "special": "photo"},
]

SYSTEM_LOG = [
    {"date": "17.04.2019", "time": "18:41", "text": "ADMIN-01 created", "hot": True},
    {"date": "17.04.2019", "time": "18:52", "text": "ADMIN-01 authentication successful"},
    {"date": "18.04.2019", "time": "02:11", "text": "ADMIN-01 owner field REDACTED", "hot": True},
    {"date": "18.04.2019", "time": "02:13", "text": "USER-017 created"},
    {"date": "18.04.2019", "time": "02:17", "text": "USER-017 first login"},
    {"date": "21.06.2020", "time": "04:22", "text": "ADMIN-01 FILE ACCESS: ADMIN_PROTOCOL.pdf"},
    {"date": "04.11.2021", "time": "22:08", "text": "USER-017 login"},
    {"date": "17.04.2022", "time": "00:00", "text": "ARCHIVE MIGRATION completed"},
    {"date": "17.04.2025", "time": "23:59", "text": "USER-017 login"},
    {"date": "21.09.2026", "time": "23:17", "text": "ADMIN-01 login successful", "hot": True},
    {"date": "21.09.2026", "time": "23:19", "text": "USER-017 login successful", "hot": True},
]

DELETED_RECORDS = [
    {"lines": [
        "[DELETED]",
        "User: USER-017",
        "Created: 18.04.2019",
        "Created by: ADMIN-01",
        "Reason: unknown",
    ]},
    {"lines": [
        "[DELETED]",
        "ADMIN-01",
        "Original owner: REDACTED",
        "Recovery: FAILED",
    ]},
    {"lines": [
        "[DELETED]",
        "C.U.",
        "External technical consultant",
        "Access level: 5",
        "Recovery: PARTIAL",
    ]},
]

CU_PROFILE = {
    "code": "C.U.",
    "role": "External technical consultant.",
    "access_level": 5,
    "authorized": ["C17", "ADMIN", "TRANSFER"],
}

ARCHIVED_DATA = {
    "2019": {"status": "unavailable", "text": "Data unavailable."},
    "2020": {"status": "files", "count": 37},
    "2021": {"status": "files", "count": 42},
    "2022": {"status": "migration", "text": "Migration completed."},
    "2023": {"status": "files", "count": 8},
    "2024": {"status": "files", "count": 3},
    "2025": {"status": "files", "count": 1},
    "2026": {"status": "restricted", "text": "ACCESS RESTRICTED"},
}

PRIVATE_NODE = {
    "title": "C-17 // PRIVATE NODE",
    "status": "ONLINE",
    "last_connection": "21.09.2026 — 23:17",
    "session": "ACTIVE SESSION",
}