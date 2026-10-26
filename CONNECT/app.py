# -*- coding: utf-8 -*-
from flask import (
    Flask, render_template, request, session,
    redirect, url_for, abort, jsonify,
)
from data import (
    SITE, PASSWORD_PUBLIC, PASSWORD_SECRET,
    LOGIN_PUBLIC, LOGIN_SECRET,
    PUBLIC_CHATS, SECRET_CHATS, CONTROL,
    DRESSES, DRESSES_NOTE, DRESSES_FOOTER, DRESSES_RENTAL,
    HUNT_SEASON, HUNTS, HUNT_SLOTS, HUNT_RULES_PENALTY,
    PANOPTICON, DEAD_DROP,
    CHAT_HIJACK, PLOT_ENDINGS, PLOT_ENDINGS_SECRET,
    BOT, QUIZ_ROUNDS, QUIZ_CONFIG,
    REQUEST_UNLOCK,
    QUIZ_FINALS, FLAG_PRIORITY,
    OD17_ACCESS, PLOT_MOTIVE_MODS, HUNT_LABYRINTH,
    PLOT_EXTRA_MODS,
    FATE_BY_KEY, PLOT_HUNT_MODS,
    REPORT,
)
import os
import json
import random
import datetime
import re
import platform


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "dev-fallback-key")

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

ALLOWED_SKUS = {d["sku"] for d in DRESSES}


# ------------------------------------------------------------------
# PER-SESSION CHAT STATE
# ------------------------------------------------------------------
def _chat_state():
    st = session.get("chat_state")
    if not isinstance(st, dict):
        st = {}
        session["chat_state"] = st
    return st


def _chat_messages(chat_id):
    st = session.get("chat_state")
    if not isinstance(st, dict):
        return []
    return st.get(chat_id, [])


def _save_chat_state(state_dict):
    session["chat_state"] = state_dict
    session.modified = True


def _clear_chat_state():
    session.pop("chat_state", None)
    session.modified = True


# ------------------------------------------------------------------
# ТРИГГЕРЫ
# ------------------------------------------------------------------
TRIGGER_PATTERNS = [
    r"admin", r"root", r"sudo", r"password", r"passwd",
    r"key", r"token", r"secret",
    r"c-?17", r"od-?17", r"connect",
    r"чон", r"хан", r"1704",
    r"<script", r"onerror", r"javascript:",
    r"\.\./", r"wp-admin", r"phpmyadmin",
]

SUSPICIOUS_PATHS = [
    "/admin", "/wp-admin", "/wp-login", "/phpmyadmin",
    "/login.php", "/.env", "/config", "/backup",
    "/db", "/sql", "/shell", "/cmd", "/control.php",
]

FORBIDDEN_CHAT_IDS = {
    "admin", "root", "system", "system01", "sysadmin",
    "dm-han", "dm-c", "u99", "u00", "u01",
    "secret", "private", "hidden", "debug",
}


def is_suspicious_text(text: str) -> bool:
    if not text:
        return False
    if len(text) > 2000:
        return True
    t = text.lower()
    for p in TRIGGER_PATTERNS:
        if re.search(p, t):
            return True
    return False


def shutdown(reason="breach"):
    session["shutdown"] = True
    session["shutdown_reason"] = reason
    _clear_chat_state()
    return redirect(url_for("shutdown_page", reason=reason))


@app.before_request
def enforce_shutdown():
    if not session.get("shutdown"):
        return
    if request.endpoint in (
        None, "static", "shutdown_page", "logout",
        "login", "root", "reset_magic",
    ):
        return
    return redirect(url_for("shutdown_page",
                            reason=session.get("shutdown_reason", "breach")))


@app.context_processor
def inject_site():
    return {"site": SITE}


def is_authed():
    return session.get("authed", False)


def is_secret():
    return session.get("secret", False)


def _now_time():
    return datetime.datetime.now().strftime("%H:%M")


def _find_chat(chat_id, chats):
    return next((c for c in chats if c["id"] == chat_id), None)


def _mark_read(chat_id):
    read = set(session.get("read_chats", []))
    read.add(chat_id)
    session["read_chats"] = list(read)
    session.modified = True


def _with_read_state(chats):
    read = set(session.get("read_chats", []))
    out = []
    for c in chats:
        c2 = dict(c)
        if c2["id"] in read:
            c2["unread"] = 0
        out.append(c2)
    return out


def _bot_reply(text: str) -> str:
    low = text.lower()
    cfg = BOT

    has_engineer = any(w in low for w in cfg.get("keywords_engineer", []))
    has_audit    = any(w in low for w in cfg.get("keywords_audit", []))
    has_status   = any(w in low for w in cfg.get("keywords_status", []))

    if has_engineer and has_audit and has_status:
        return "__BROKEN__"

    if has_engineer and has_audit:
        return cfg["partial_engineer"]

    if has_engineer:
        return cfg["partial_audit"]

    return cfg["deny"]


# ------------------------------------------------------------------
# SYNAPSE-ASSISTANT — 30 вопросов, метаданные, флаги, финал
# ------------------------------------------------------------------
def _collect_server_meta():
    try:
        sys_user = os.environ.get("USERNAME") or os.environ.get("USER") or "anon"
    except Exception:
        sys_user = "anon"

    now = datetime.datetime.now()
    hour = now.hour
    if 4 <= hour < 12:
        time_of_day = "утро"
    elif 12 <= hour < 17:
        time_of_day = "день"
    elif 17 <= hour < 23:
        time_of_day = "вечер"
    else:
        time_of_day = "ночь"

    return {
        "sys_user": sys_user,
        "os_name": platform.system(),
        "time_of_day": time_of_day,
        "now_time": now.strftime("%H:%M"),
    }


def _collect_client_meta():
    return session.get("client_meta", {}) or {}


def _count_ip_sessions():
    ip = request.remote_addr or "0.0.0.0"
    counter = session.get("ip_counter", {})
    if not isinstance(counter, dict):
        counter = {}
    return int(counter.get(ip, 0))


def _bump_ip_sessions():
    ip = request.remote_addr or "0.0.0.0"
    counter = session.get("ip_counter", {})
    if not isinstance(counter, dict):
        counter = {}
    counter[ip] = int(counter.get(ip, 0)) + 1
    session["ip_counter"] = counter
    session.modified = True


def _resolve_question(item, step):
    srv = _collect_server_meta()
    cli = _collect_client_meta()

    if "branch_from" in item:
        prev_id = item["branch_from"]
        prev_choice = session.get(f"answer_{prev_id}", "a")
        q = item["question_yes"] if prev_choice == "a" else item["question_no"]
    else:
        q = item["question"]

    repl = {
        "{sys_user}":     srv["sys_user"],
        "{time_of_day}":  srv["time_of_day"],
        "{time}":         srv["now_time"],
        "{screen}":       cli.get("screen", "неизвестно"),
        "{browser}":      cli.get("browser", "неизвестно"),
        "{tz}":           cli.get("tz", "неизвестно"),
        "{lang}":         cli.get("lang", "неизвестно"),
        "{ip_sessions}":  str(max(0, _count_ip_sessions() - 1)),
        "{user}":         srv["sys_user"],
    }
    for k, v in repl.items():
        q = q.replace(k, v)
    return q


def _pick_final(flags):
    # все "да" → секретная концовка
    all_yes = all(session.get(f"answer_{i}") == "a" for i in range(1, 31))
    if all_yes:
        return QUIZ_FINALS["secret_x"]

    if not flags:
        return QUIZ_FINALS.get("silent") or QUIZ_FINALS["isolation"]

    # доминирующий флаг = максимум по количеству;
    # при равенстве — порядок FLAG_PRIORITY
    best_flag = None
    best_count = -1
    for f in FLAG_PRIORITY:
        cnt = flags.get(f, 0)
        if cnt > best_count:
            best_count = cnt
            best_flag = f

    if best_flag and best_flag in QUIZ_FINALS:
        return QUIZ_FINALS[best_flag]

    for f in FLAG_PRIORITY:
        if f in flags and f in QUIZ_FINALS:
            return QUIZ_FINALS[f]

    return QUIZ_FINALS["isolation"]


def _bot_quiz(item):
    chat_id = item["id"]
    _mark_read(chat_id)

    if "quiz_step" not in session:
        session["quiz_step"] = 0
        session["quiz_flags"] = {}
        session["quiz_answers"] = {}
        session["bot_cracked"] = False
        session["quiz_meta_sent"] = False
        _bump_ip_sessions()

    if request.method == "POST":
        action = request.form.get("action", "answer")

        if action == "meta":
            session["client_meta"] = {
                "screen":  request.form.get("screen", "неизвестно"),
                "tz":      request.form.get("tz", "неизвестно"),
                "lang":    request.form.get("lang", "неизвестно"),
                "browser": request.form.get("browser", "неизвестно"),
                "online":  request.form.get("online", "true"),
            }
            session.modified = True
            return jsonify({"ok": True})

        if session.get("bot_cracked"):
            return jsonify({
                "status": "cracked",
                "final": session.get("quiz_final"),
            })

        step = session["quiz_step"]
        if step >= QUIZ_CONFIG["total_rounds"]:
            flags = session.get("quiz_flags", {})
            final = _pick_final(flags)
            session["bot_cracked"] = True
            session["quiz_final"] = final
            session["quiz_key"] = final.get("key", "isolation")
            frag = final.get("fragment", "C1-17-X")
            frags = set(session.get("found_fragments", []))
            frags.add(frag)
            session["found_fragments"] = list(frags)
            session.modified = True
            return jsonify({
                "status": "victory",
                "final": final,
                "flags": flags,
            })

        choice = request.form.get("choice", "")
        r_now = QUIZ_ROUNDS[step]

        if r_now.get("no_options"):
            session["quiz_step"] = step + 1
            session.modified = True
            return jsonify({"status": "next", **_next_payload(step + 1)})

        flags = session.get("quiz_flags", {})

        if choice == "a" and r_now.get("flags_yes"):
            for f in r_now["flags_yes"]:
                flags[f] = flags.get(f, 0) + 1

        if r_now.get("flags_by_choice"):
            f = r_now["flags_by_choice"].get(choice)
            if f:
                flags[f] = flags.get(f, 0) + 1

        session["quiz_flags"] = flags

        answers = session.get("quiz_answers", {})
        answers[str(r_now["id"])] = choice
        session[f"answer_{r_now['id']}"] = choice
        session["quiz_answers"] = answers
        session["quiz_step"] = step + 1
        session.modified = True

        voice_key = "voice_yes" if choice == "a" else "voice_no"
        voice_text = r_now.get(voice_key, "")

        if session["quiz_step"] >= QUIZ_CONFIG["total_rounds"]:
            flags = session.get("quiz_flags", {})
            final = _pick_final(flags)
            session["bot_cracked"] = True
            session["quiz_final"] = final
            session["quiz_key"] = final.get("key", "isolation")
            frag = final.get("fragment", "C1-17-X")
            frags = set(session.get("found_fragments", []))
            frags.add(frag)
            session["found_fragments"] = list(frags)
            session.modified = True
            return jsonify({
                "status": "victory",
                "final": final,
                "flags": flags,
                "voice": voice_text,
            })

        return jsonify({
            "status": "next",
            "voice": voice_text,
            **_next_payload(session["quiz_step"]),
        })

    if session.get("bot_cracked"):
        final = session.get("quiz_final") or QUIZ_FINALS["isolation"]
        return render_template(
            "chat.html",
            chat=item, chats=_with_read_state(PUBLIC_CHATS),
            extra=[], director_online=False, deactivated=True,
            deactivated_seen=bool(session.get("deactivated_seen")),
            animate=False,
            bot_cracked=True,
            bot_final=final,
            od17=OD17_ACCESS,
        )

    step = session["quiz_step"]
    if step >= QUIZ_CONFIG["total_rounds"]:
        step = 0
        session["quiz_step"] = 0
        session.modified = True

    r_now = QUIZ_ROUNDS[step]
    question_text = _resolve_question(r_now, step)

    return render_template(
        "chat.html",
        chat=item, chats=_with_read_state(PUBLIC_CHATS),
        extra=[], director_online=False, deactivated=True,
        deactivated_seen=bool(session.get("deactivated_seen")),
        animate=False,
        bot_cracked=False,
        quiz={
            "step": step,
            "total": QUIZ_CONFIG["total_rounds"],
            "percent": round(step / QUIZ_CONFIG["total_rounds"] * 100),
            "act": r_now.get("act", 1),
            "no_options": r_now.get("no_options", False),
            "pause_after": r_now.get("pause_after", 0),
            "question": question_text,
            "options": r_now["options"],
        },
    )


def _next_payload(step):
    if step >= QUIZ_CONFIG["total_rounds"]:
        return {}
    r = QUIZ_ROUNDS[step]
    q = _resolve_question(r, step)
    return {
        "step": step + 1,
        "total": QUIZ_CONFIG["total_rounds"],
        "percent": round(step / QUIZ_CONFIG["total_rounds"] * 100),
        "act": r.get("act", 1),
        "no_options": r.get("no_options", False),
        "pause_after": r.get("pause_after", 0),
        "question": q,
        "options": r["options"],
    }


@app.route("/bot/meta", methods=["POST"])
def bot_meta():
    if not is_authed():
        return jsonify({"ok": False}), 403
    session["client_meta"] = {
        "screen":  request.form.get("screen", "неизвестно"),
        "tz":      request.form.get("tz", "неизвестно"),
        "lang":    request.form.get("lang", "неизвестно"),
        "browser": request.form.get("browser", "неизвестно"),
        "online":  request.form.get("online", "true"),
    }
    session.modified = True
    return jsonify({"ok": True})


# ------------------------------------------------------------------
# HIJACK
# ------------------------------------------------------------------

# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
# HIJACK  (в app.py замените старую функцию _evaluate_hijack этим блоком;
# _norm_id оставьте как есть. Нужные импорты уже есть: re, CHAT_HIJACK)
# ------------------------------------------------------------------
def _strip(s):
    return re.sub(r"[\s\.\-_]", "", (s or "").lower().replace("ё", "е"))


def _match_role(name):
    """melnikov и lev проверяются первыми, короткие шаблоны (<=3 символов) — только точно."""
    pats = CHAT_HIJACK["name_patterns"]
    norm = _strip(name)
    order = ["melnikov", "lev"] + [k for k in pats if k not in ("melnikov", "lev")]
    for key in order:
        for p in pats.get(key, []):
            pn = _strip(p)
            if not pn:
                continue
            if len(pn) <= 3:
                if norm == pn:
                    return key
            elif pn in norm:
                return key
    return "unknown"


def _evaluate_hijack(chain, values):
    cfg = CHAT_HIJACK
    intents = cfg["intents"]
    given_id = (values.get("name_self") or "").strip()
    chain = [c for c in chain if c in intents]

    # kill-кубики срабатывают сразу
    for c in chain:
        if intents[c].get("kill"):
            return {"status": "kill", "key": c,
                    "msg": cfg["kill_reactions"].get(c, "неизвестная ошибка.")}

    # ровно по одному кубику из каждой из 4 строк
    rows = {}
    for c in chain:
        rows.setdefault(intents[c]["order"], []).append(c)
    if sorted(rows) != [1, 2, 3, 4] or any(len(v) != 1 for v in rows.values()):
        return {"status": "bad", "key": "incomplete",
                "msg": cfg["soft_errors"]["incomplete"]}
    if not given_id:
        return {"status": "bad", "key": "no_name",
                "msg": cfg["soft_errors"]["no_name"]}

    role = _match_role(given_id)
    low = given_id.lower()

    if role == "chon":
        return {"status": "kill", "key": "name_chon",
                "msg": cfg["kill_reactions"]["name_chon"]}

    real_name = next((rn for rn in cfg["real_names"] if rn in low), None)

    role_arch = "мусор"
    for arch in ("свой", "милана", "силовик", "руководство",
                 "работник", "журналист", "слабый", "чужой"):
        if role in cfg["role_groups"].get(arch, []):
            role_arch = arch
            break

    entry_id = rows[2][0]
    tone = intents[rows[3][0]].get("tone", "business")
    temp = intents[rows[4][0]].get("temp", "info")

    tone_arch = next((a for a, t in cfg["tone_groups"].items() if tone in t), "дело")
    temp_arch = next((a for a, t in cfg["temp_groups"].items() if temp in t), "инфо")

    parts = [f"Я {given_id}."] + [
        intents[c]["phrase"] for c in chain
        if c != "name_self" and intents[c].get("phrase")
    ]
    phrase = " ".join(parts)

    base_msg = (cfg["special_reactions"].get(role)
                or cfg["role_reactions"][role_arch])
    entry_mod = cfg["entry_mods"].get(entry_id, "")
    if entry_mod:
        base_msg = entry_mod + "\n" + base_msg

    if real_name:
        base_msg = (
            f"{real_name.upper()}.\n"
            "я знаю.\n"
            "я знаю всех, кто в этой комнате.\n"
            "ты не первый, кто пробует.\n"
            "и не последний."
        )

    ROLE_CODE = {"свой": "A", "чужой": "B", "работник": "C", "руководство": "D",
                 "силовик": "E", "журналист": "F", "слабый": "G",
                 "милана": "H", "мусор": "X"}

    return {
        "status": "ok",
        "key": role_arch,
        "role": role,
        "family": cfg.get("family_by_role", {}).get(role, "unknown"),
        "tone": tone_arch,
        "temp": temp_arch,
 # ------------------------------------------------------------------
# "tone_mod": tone_mod,
# "temp_mod": temp_mod,
# ------------------------------------------------------------------
        "msg": base_msg,
        "phrase": phrase,
        "given_id": given_id,
        "fragment": f"04-M-{ROLE_CODE.get(role_arch, 'X')}",
        "real_name": real_name,
    }

def _norm_id(s: str) -> str:
    return re.sub(r"[\s\.\-_]", "", (s or "").lower())


# ------------------------------------------------------------------
# КОНЦОВКА: строка роли + строка судьбы + модификаторы
# ------------------------------------------------------------------
def _panopticon_key():
    """Три исхода паноптикона: сообщил / увидел и промолчал / не увидел."""
    if session.get("panopticon_rescued"):
        return "panopticon_rescued"
    if session.get("panopticon_found"):
        return "panopticon_ignored"
    return "panopticon_missed"


def _plot_mods(motive_arch, fate):
    """Модификаторы: мотив из каталога, охота (зависит от судьбы Миланы), паноптикон."""
    mods = []

    motive = PLOT_MOTIVE_MODS.get(motive_arch, "")
    if motive:
        mods.append(motive)

    hunt = session.get("hunt_choice")
    hunt_mod = PLOT_HUNT_MODS.get(hunt, {}).get(fate, "")
    if hunt_mod:
        mods.append(hunt_mod)

    pan_mod = PLOT_EXTRA_MODS.get(_panopticon_key(), "")
    if pan_mod:
        mods.append(pan_mod)

    return mods


def _get_plot_ending(role_group, quiz_key, motive_arch="use"):
    # Секретные
    if role_group == "свой" and quiz_key == "secret_x":
        given = (session.get("hijack_given_id") or "").lower()
        if "c.u" in given or "cu" == given.replace(".", ""):
            return PLOT_ENDINGS_SECRET["cu_secret"]
    if role_group == "милана" and quiz_key == "loss_of_self":
        return PLOT_ENDINGS_SECRET["milana_secret"]

    base = PLOT_ENDINGS.get((role_group, quiz_key)) or "Конец. Никто не знает, что было."
    fate = FATE_BY_KEY.get(quiz_key, "held")

    mods = _plot_mods(motive_arch, fate)
    return base + ("\n\n" + "\n\n".join(mods) if mods else "")


# ------------------------------------------------------------------
# OPAQUE URL
# ------------------------------------------------------------------
RESERVED = {
    "login", "logout", "inbox", "chat", "catalog", "hunt",
    "panopticon", "sanitizer", "dead_drop", "control",
    "shutdown", "reset", "transition", "static", "favicon.ico",
}


def _remember(kind, arg=None):
    session["page_kind"] = kind
    if arg is None:
        session.pop("page_arg", None)
    else:
        session["page_arg"] = arg


@app.route("/<slug>", methods=["GET", "POST"])
def opaque(slug):
    if slug in RESERVED:
        abort(404)
    if not is_secret():
        return redirect(url_for("login"))

    kind = session.get("page_kind")
    arg = session.get("page_arg")

    if not kind:
        return redirect(url_for("inbox"))

    if kind == "inbox":
        return inbox()
    if kind == "chat":
        return chat(arg)
    if kind == "catalog":
        return catalog()
    if kind == "hunt":
        return hunt()
    if kind == "hunt_item":
        return hunt_item(arg)
    if kind == "panopticon":
        return panopticon()
    if kind == "sanitizer":
        return sanitizer()
    if kind == "dead_drop":
        return dead_drop()

    return redirect(url_for("inbox"))


# ------------------------------------------------------------------
# RESET
# ------------------------------------------------------------------
@app.route("/reset")
def reset_magic():
    session.clear()
    return redirect(url_for("login"))


@app.route("/reset-hijack")
def reset_hijack():
    for k in ("hijack_done", "hijack_killed", "hijack_state", "frag_04_found"):
        session.pop(k, None)
    session.modified = True
    return redirect(url_for("chat_hijack", chat_id=CHAT_HIJACK["chat_id"]))


@app.route("/reset-panopticon")
def reset_panopticon():
    """Сброс только паноптикона (для тестов): решение, спасение, разблокировку CAM-05."""
    if not is_secret():
        return redirect(url_for("inbox"))
    for k in ("panopticon_decided", "panopticon_rescued", "panopticon_found",
              "panopticon_CAM-05_unlocked", "panopticon_CAM-05_settings"):
        session.pop(k, None)
    session.modified = True
    return redirect(url_for("panopticon"))


# ------------------------------------------------------------------
# Логин
# ------------------------------------------------------------------
@app.route("/", methods=["GET"])
def root():
    if session.get("shutdown"):
        session.clear()
    if not is_authed():
        return redirect(url_for("login"))
    return redirect(url_for("inbox"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET" and session.get("shutdown"):
        session.clear()

    if request.method == "POST":
        user = request.form.get("login", "").strip().lower()
        pwd  = request.form.get("password", "").strip()

        if len(user) > 100 or len(pwd) > 100:
            return shutdown(reason="breach")

        if is_suspicious_text(pwd) and pwd not in (PASSWORD_SECRET, PASSWORD_PUBLIC):
            return shutdown(reason="keyword")

        if user == LOGIN_SECRET and pwd == PASSWORD_SECRET:
            session["authed"] = True
            session["secret"] = True
            session["fails"] = 0
            return redirect(url_for("transition"))

        if user == LOGIN_PUBLIC and pwd == PASSWORD_PUBLIC:
            session["authed"] = True
            session["secret"] = False
            session["fails"] = 0
            return redirect(url_for("inbox"))

        session["fails"] = session.get("fails", 0) + 1
        if session["fails"] >= 3:
            return shutdown(reason="bruteforce")

        return render_template("login.html", error=True)

    return render_template("login.html", error=False)


@app.route("/logout")
def logout():
    saved = {
        "found_fragments":    session.get("found_fragments", []),
        "hijack_role":        session.get("hijack_role"),
        "hijack_fragment":    session.get("hijack_fragment"),
        "hijack_given_id":    session.get("hijack_given_id"),
        "quiz_key":           session.get("quiz_key"),
        "quiz_final":         session.get("quiz_final"),
        "panopticon_found":   session.get("panopticon_found"),
        "panopticon_decided": session.get("panopticon_decided"),
        "panopticon_rescued": session.get("panopticon_rescued"),
        "hunt_choice":        session.get("hunt_choice"),
        "hunt_finished":      session.get("hunt_finished"),
        "dress_motive_arch":  session.get("dress_motive_arch"),
        "dress_motivation":   session.get("dress_motivation"),
    }
    session.clear()
    for k, v in saved.items():
        if v is not None:
            session[k] = v
    session.modified = True
    return redirect(url_for("login"))


@app.route("/transition")
def transition():
    if not is_secret():
        return redirect(url_for("inbox"))
    return render_template("transition.html")


# ------------------------------------------------------------------
# Inbox
# ------------------------------------------------------------------
@app.route("/inbox")
def inbox():
    if not is_authed():
        return redirect(url_for("login"))
    _remember("inbox")

    deactivated      = bool(session.get("account_deactivated"))
    deactivated_seen = bool(session.get("deactivated_seen"))

    if is_secret():
        return render_template(
            "inbox_secret.html",
            chats=_with_read_state(SECRET_CHATS),
            deactivated=deactivated,
            deactivated_seen=deactivated_seen,
        )
    return render_template(
        "inbox.html",
        chats=_with_read_state(PUBLIC_CHATS),
        deactivated=deactivated,
        deactivated_seen=deactivated_seen,
    )


# ------------------------------------------------------------------
# Каталог
# ------------------------------------------------------------------
@app.route("/catalog")
def catalog():
    if not is_secret():
        return redirect(url_for("inbox"))
    _remember("catalog")
    return render_template(
        "catalog.html",
        dresses=DRESSES,
        note=DRESSES_NOTE,
        footer=DRESSES_FOOTER,
        chats=SECRET_CHATS,
    )


# ------------------------------------------------------------------
# ЧАТ
# ------------------------------------------------------------------
@app.route("/chat/<chat_id>", methods=["GET", "POST"])
def chat(chat_id):
    if not is_authed():
        return redirect(url_for("login"))

    _remember("chat", chat_id)

    if chat_id in FORBIDDEN_CHAT_IDS:
        return shutdown(reason="breach")

    if is_secret():
        item = _find_chat(chat_id, SECRET_CHATS)
        if not item:
            return shutdown(reason="breach")

        if request.method == "POST":
            if not item.get("writable", True):
                return redirect(url_for("chat", chat_id=chat_id))
            text = request.form.get("text", "").strip()
            if text:
                now = _now_time()
                st = _chat_state()
                st.setdefault(chat_id, []).append(
                    {"from": "me", "text": text, "time": now}
                )
                _save_chat_state(st)
            return redirect(url_for("chat", chat_id=chat_id))

        _mark_read(chat_id)
        extra = _chat_messages(chat_id)

        hijack_offer = (
            chat_id == CHAT_HIJACK["chat_id"]
            and not session.get("hijack_done")
            and not session.get("hijack_killed")
        )

        return render_template(
            "chat_secret.html",
            chat=item, chats=_with_read_state(SECRET_CHATS),
            extra=extra, animate=False,
            hijack_offer=hijack_offer,
        )

    item = _find_chat(chat_id, PUBLIC_CHATS)
    if not item:
        return shutdown(reason="breach")

    if item.get("bot") and session.get("account_deactivated"):
        return _bot_quiz(item)

    is_director = bool(item.get("director"))
    account_deactivated = bool(session.get("account_deactivated"))

    chat_state = _chat_state()
    state = chat_state.setdefault(chat_id, [])

    if request.method == "POST":
        if account_deactivated:
            return redirect(url_for("chat", chat_id=chat_id))
        if not item.get("writable"):
            return redirect(url_for("chat", chat_id=chat_id))

        text = request.form.get("text", "").strip()
        if text:
            now = _now_time()
            state.append({"from": "me", "text": text, "time": now})

            if item.get("bot"):
                reply = _bot_reply(text)
                if reply == "__BROKEN__":
                    reply = BOT["deny"]
                state.append({"from": "them", "text": reply, "time": now})

            elif is_director and not session.get("account_deactivated"):
                threats = [
                    "КТО ЭТО БЛЯТЬ ТУТ",
                    "Кто сидит за аккаунтом Миланы Макаровой?",
                    "Макарова задержана час назад.",
                    "Аккаунт будет деактивирован.",
                ]
                for t in threats:
                    state.append({
                        "from": "them", "text": t, "time": now, "pending": True
                    })

                state.append({
                    "from": "system", "text": "ACCOUNT DEACTIVATED",
                    "time": "", "pending": True
                })

                session["account_deactivated"] = True
                session["deactivated_seen"] = True
                session["anim_pending_" + chat_id] = True

        _save_chat_state(chat_state)
        return redirect(url_for("chat", chat_id=chat_id))

    _mark_read(chat_id)
    animate = bool(session.pop("anim_pending_" + chat_id, False))
    session.modified = True
    director_online = is_director
    deactivated_seen = bool(session.get("deactivated_seen"))

    return render_template(
        "chat.html",
        chat=item, chats=_with_read_state(PUBLIC_CHATS),
        extra=state,
        director_online=director_online,
        deactivated=account_deactivated,
        deactivated_seen=deactivated_seen,
        animate=animate,
        bot_cracked=bool(session.get("bot_cracked") and item.get("bot")),
    )


# ------------------------------------------------------------------
# CHAT HIJACK
# ------------------------------------------------------------------
@app.route("/chat/<chat_id>/hijack", methods=["GET", "POST"])
def chat_hijack(chat_id):
    if not is_secret():
        return redirect(url_for("inbox"))

    if chat_id != CHAT_HIJACK["chat_id"]:
        return shutdown(reason="breach")

    if session.get("hijack_killed"):
        return render_template(
            "chat_hijack_dead.html",
            cfg=CHAT_HIJACK,
            chat=_find_chat(chat_id, SECRET_CHATS),
        )

    state = session.get("hijack_state", {})
    state.setdefault("chain", [])
    state.setdefault("values", {})
    state.setdefault("impostor_lines", list(CHAT_HIJACK["intro_system"]))
    state.setdefault("user_messages", [])

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "hijack_submit":
            try:
                chain = json.loads(request.form.get("chain", "[]"))
            except Exception:
                chain = []

            values = {}
            for k in request.form:
                if k.startswith("value_"):
                    values[k[len("value_"):]] = request.form[k].strip()

            verdict = _evaluate_hijack(chain, values)

            if verdict.get("phrase"):
                state["user_messages"].append({
                    "from": "me", "text": verdict["phrase"],
                })

            if verdict["status"] == "ok":
                session["hijack_done"] = True
                session["frag_04_found"] = True
                session["hijack_given_id"] = verdict.get("given_id") or ""
                session["hijack_role"] = verdict["key"]

                frag = verdict["fragment"]
                frags = set(session.get("found_fragments", []))
                frags.add(frag)
                session["found_fragments"] = list(frags)
                session["hijack_fragment"] = frag

                for line in verdict["msg"].split("\n"):
                    state["user_messages"].append({
                        "from": "them",
                        "author": CHAT_HIJACK["impostor"],
                        "text": line,
                    })

                state["verdict"] = verdict
                session["hijack_state"] = state
                session.modified = True
                return redirect(url_for("chat_hijack", chat_id=chat_id))

            if verdict["status"] == "kill":
                session["hijack_killed"] = True
                for line in verdict["msg"].split("\n"):
                    state["user_messages"].append({
                        "from": "them",
                        "author": CHAT_HIJACK["impostor"],
                        "text": line,
                        "kill": True,
                    })
                state["verdict"] = verdict
                session["hijack_state"] = state
                session.modified = True
                return redirect(url_for("chat_hijack", chat_id=chat_id))

            for line in verdict["msg"].split("\n"):
                state["user_messages"].append({
                    "from": "them",
                    "author": CHAT_HIJACK["impostor"],
                    "text": line,
                })
            state["verdict"] = verdict
            state["chain"] = []
            state["values"] = {}
            session["hijack_state"] = state
            session.modified = True
            return redirect(url_for("chat_hijack", chat_id=chat_id))

        if action == "reset_chain":
            state["chain"] = []
            state["values"] = {}
            session["hijack_state"] = state
            session.modified = True
            return redirect(url_for("chat_hijack", chat_id=chat_id))

    session["hijack_state"] = state
    session.modified = True

    return render_template(
        "chat_hijack.html",
        cfg=CHAT_HIJACK,
        chat=_find_chat(chat_id, SECRET_CHATS),
        state=state,
        hijack_fragment=session.get("hijack_fragment", ""),
    )


# ------------------------------------------------------------------
# Платья
# ------------------------------------------------------------------
def _is_request_dress(item):
    return "запрос" in (item.get("price") or "").lower()


@app.route("/catalog/<sku>")
def dress(sku):
    if not is_secret():
        return redirect(url_for("inbox"))

    if sku not in ALLOWED_SKUS:
        return shutdown(reason="breach")

    item = next((d for d in DRESSES if d["sku"] == sku), None)
    if not item:
        return shutdown(reason="breach")

    _remember("catalog")

    is_req = _is_request_dress(item)

    return render_template(
        "dress.html",
        dress=item,
        rental=DRESSES_RENTAL,
        chats=SECRET_CHATS,
        request_unlock=REQUEST_UNLOCK,
        is_request=is_req,
        unlocked=bool(session.get("dress_motivation")),   # было frag_04_found
        motivation=session.get("dress_motivation"),
        fragment=session.get("dress_fragment"),
    )


# Мотивации → фрагмент
MOTIVE_FRAGMENTS = {
    "Освободить её": "FRAG-FREE-17",
    "Скрыть от системы": "FRAG-HIDE-17",
    "Забрать себе": "FRAG-SELF-17",
    "Использовать для шантажа": "FRAG-BLACK-17",
    "Выкупить контракт": "FRAG-BUY-17",
    "Перепродать конкурентам": "FRAG-SELL-17",
    "Улучшить (апгрейд)": "FRAG-UPG-17",
    "Перепрограммировать": "FRAG-CODE-17",
    "Уничтожить данные": "FRAG-DEL-17",
    "Стереть её личность": "FRAG-WIPE-17",
    "Вскрыть систему изнутри": "FRAG-HACK-17",
    "Узнать правду о C-17": "FRAG-TRUTH-17",
}

# Архетипы мотивации
SAVE_MOTIVES    = ["Освободить её", "Скрыть от системы", "Узнать правду о C-17"]
USE_MOTIVES     = ["Забрать себе", "Использовать для шантажа", "Перепродать конкурентам",
                   "Выкупить контракт", "Улучшить (апгрейд)", "Перепрограммировать"]
DESTROY_MOTIVES = ["Уничтожить данные", "Стереть её личность", "Вскрыть систему изнутри"]

def _hunt_reply(state, hid):
    session[HUNT_STATE_KEY] = state
    session.modified = True
    if _wants_json():
        return _json_state(state)
    return redirect(url_for("hunt_game", hid=hid))

@app.route("/catalog/<sku>/request", methods=["POST"])
def dress_request(sku):
    if not is_secret():
        return jsonify({"ok": False, "msg": "ACCESS DENIED"}), 403

    if sku not in ALLOWED_SKUS:
        return jsonify({"ok": False, "msg": "NOT FOUND"}), 404

    motivation = request.form.get("motivation", "")

    if not motivation:
        return jsonify({"ok": False, "msg": "ЦЕЛЬ НЕ УКАЗАНА."})

    fragment = MOTIVE_FRAGMENTS.get(motivation, "FRAG-UNK-17")

    if motivation in SAVE_MOTIVES:
        motive_arch = "save"
    elif motivation in DESTROY_MOTIVES:
        motive_arch = "destroy"
    else:
        motive_arch = "use"   # USE_MOTIVES и всё неизвестное

    session["dress_motivation"] = motivation
    session["dress_motive_arch"] = motive_arch
    session["dress_fragment"] = fragment

    frags = set(session.get("found_fragments", []))
    frags.add(fragment)
    session["found_fragments"] = list(frags)
    session.modified = True

    return jsonify({
        "ok": True,
        "fragment": fragment,
        "msg": REQUEST_UNLOCK["success_text"],
        "motivation": motivation
    })


@app.route("/catalog/<sku>/order", methods=["GET", "POST"])
def order(sku):
    if not is_secret():
        return redirect(url_for("inbox"))

    if sku not in ALLOWED_SKUS:
        return shutdown(reason="breach")

    item = next((d for d in DRESSES if d["sku"] == sku), None)
    if not item:
        return shutdown(reason="breach")

    _remember("catalog")

    if request.method == "POST":
        form = {
            "address": request.form.get("address", "").strip(),
            "date":    request.form.get("date", "").strip(),
            "slot":    request.form.get("slot", "").strip(),
            "hours":   request.form.get("hours", "").strip(),
            "notes":   request.form.get("notes", "").strip(),
            "payment": request.form.get("payment", "on_delivery").strip(),
        }

        for v in form.values():
            if is_suspicious_text(v):
                return shutdown(reason="keyword")

        order_id = f"ORD-{random.randint(1700, 1799)}"

        DISCOUNT = 0.20
        subtotal = 0.0
        discount = 0.0
        total_val = 0.0

        try:
            num = float(item.get("price", "").split()[0])
            hours = float(form["hours"] or 0)
            subtotal  = num * hours
            discount  = subtotal * DISCOUNT
            total_val = subtotal - discount
        except Exception:
            pass

        def fmt(x):
            s = f"{x:.2f}"
            return s.rstrip('0').rstrip('.') if '.' in s else s

        subtotal_str = fmt(subtotal) + " USDT"
        discount_str = "−" + fmt(discount) + " USDT"
        total        = fmt(total_val) + " USDT"

        now = _now_time()

        pay_label = ("Оплата при получении"
                     if form.get("payment") == "on_delivery"
                     else "Оплата сейчас")

        st = _chat_state()
        st.setdefault("orders", []).append({
            "from": "them",
            "author": "ORDERS",
            "time": now,
            "hot": True,
            "text": (
                f"Заказ оформлен.\n"
                f"Номер: {order_id}\n"
                f"Позиция: {item['title']} ({sku})\n"
                f"Точка: {form['address']}\n"
                f"Дата: {form['date']} · {form['slot']}\n"
                f"Срок: {form['hours']} ч.\n"
                f"Подытог: {subtotal_str}\n"
                f"Скидка сотрудника −20%: {discount_str}\n"
                f"Сумма: {total}\n"
                f"Оплата: {pay_label}"
            ),
        })
        _save_chat_state(st)

        session["last_order_id"] = order_id
        session.modified = True

        return render_template(
            "order_success.html",
            dress=item,
            order=form,
            order_id=order_id,
            rental=DRESSES_RENTAL,
            subtotal=subtotal_str,
            discount=discount_str,
            total=total,
        )

    return render_template(
        "order.html",
        dress=item,
        rental=DRESSES_RENTAL,
        chats=SECRET_CHATS,
    )


@app.route("/shutdown")
def shutdown_page():
    reason = request.args.get("reason") or session.get("shutdown_reason") or "breach"
    session["shutdown"] = True
    session["shutdown_reason"] = reason
    return render_template("shutdown.html", reason=reason)


@app.route("/control")
def control():
    if not is_secret():
        return shutdown(reason="breach")
    _remember("inbox")
    return render_template("control.html", control=CONTROL, chats=SECRET_CHATS)


@app.errorhandler(404)
def not_found(_e):
    path = (request.path or "").lower()
    for p in SUSPICIOUS_PATHS:
        if path.startswith(p):
            return shutdown(reason="breach")
    return render_template("404.html"), 404


# ------------------------------------------------------------------
# THE HUNT
# ------------------------------------------------------------------
@app.route("/hunt")
def hunt():
    if not is_secret():
        return redirect(url_for("inbox"))
    _remember("hunt")
    return render_template(
        "hunt.html",
        season=HUNT_SEASON,
        hunts=HUNTS,
        chats=SECRET_CHATS,
    )


import hunt_engine as eng   # hunt_engine.py лежит рядом с app.py

HUNT_GAME_TEMPLATE = "hunt_game.html"
HUNT_STATE_KEY = "hunt_state_v3"      # новый ключ: старые партии просто сбросятся


def _int(v, default=0):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _state_ok(state, hid):
    return (
        isinstance(state, dict)
        and state.get("hid") == hid
        and "seed" in state
        and "inv" in state
        and "pickups" in state
        and isinstance(state.get("target"), dict)
        and "pos" in state["target"]
        and isinstance(state.get("guards"), list)
    )


@app.route("/hunt/<hid>", methods=["GET", "POST"])
def hunt_item(hid):
    if not is_secret():
        return redirect(url_for("inbox"))

    if not re.fullmatch(r"HT-17(0[1-9]|[1-4][0-9]|50)", hid):
        return shutdown(reason="breach")

    item = HUNTS.get(hid)
    if not item:
        return shutdown(reason="breach")

    _remember("hunt_item", hid)

    if request.method == "POST":
        callsign = request.form.get("callsign", "").strip()
        slot_id  = request.form.get("slot", "").strip()

        if is_suspicious_text(callsign):
            return shutdown(reason="keyword")

        banned = ["чон", "хан", "джин", "1704", "admin", "root",
                  "полиция", "фбр", "интерпол", "журналист",
                  "лебедева", "утечка", "слив"]
        low = callsign.lower()
        for w in banned:
            if w in low:
                return shutdown(reason="breach")

        if item["status"] != "OPEN":
            return render_template(
                "hunt_reject.html",
                hunt=item,
                hunt_id=hid,
                reason="ВЫЕЗД НЕ ПРИНИМАЕТ НОВЫЕ ПОЗИЦИИ",
            )

        return render_template(
            "hunt_trace.html",
            hunt=item,
            hunt_id=hid,
            callsign=callsign or "anon",
            slot=slot_id or "S-03",
        )

    return render_template(
        "hunt_item.html",
        hunt=item,
        hunt_id=hid,
        slots=HUNT_SLOTS,
        penalty=HUNT_RULES_PENALTY,
        chats=SECRET_CHATS,
    )


def _wants_json():
    return request.headers.get("X-Requested-With") == "fetch"


def _json_state(state):
    _, game = eng.public_view(state)
    return jsonify(game)


@app.route("/hunt/<hid>/game", methods=["GET", "POST"])
def hunt_game(hid):
    if not is_secret():
        return redirect(url_for("inbox"))

    if hid not in HUNTS:
        return redirect(url_for("hunt"))

    state = session.get(HUNT_STATE_KEY)

    if request.method == "POST":
        action = request.form.get("action")

        if action in ("start", "", None):
            state = eng.new_game()
            state["hid"] = hid
            state["callsign"] = request.form.get("callsign", "")[:32]
            state["slot"] = request.form.get("slot", "")
            session[HUNT_STATE_KEY] = state
            session.pop("hunt_choice", None)
            session.pop("hunt_finished", None)
            session.modified = True
            return redirect(url_for("hunt_game", hid=hid))

        if not _state_ok(state, hid):
            session.pop(HUNT_STATE_KEY, None)
            return redirect(url_for("hunt_item", hid=hid))

        if action == "move":
            dx = max(-1, min(1, _int(request.form.get("dx"))))
            dy = max(-1, min(1, _int(request.form.get("dy"))))
            eng.step(state, dx, dy)
            return _hunt_reply(state, hid)

        if action == "use":
            eng.step(state, 0, 0, use=request.form.get("item", ""))
            return _hunt_reply(state, hid)

        if action == "chase_done":
            if state["status"] == "chase" and request.form.get("result") == "win":
                eng.finish_chase(state, True)
            return _hunt_reply(state, hid)

        # егерь наступил: сдаться или победить в перестрелке
        if action in ("surrender", "duel_win") and state["status"] == "caught":
            choice = "surrender" if action == "surrender" else "kill"
            session["hunt_choice"] = choice
            session["hunt_finished"] = True

            frag = "HT-SURRENDER" if choice == "surrender" else "HT-KILL"
            frags = set(session.get("found_fragments", []))
            frags.add(frag)
            session["found_fragments"] = list(frags)

            session.modified = True
            return redirect(url_for("hunt_game_result"))

        if action == "choice" and state["status"] == "found":
            choice = request.form.get("choice")
            if choice in ("reveal", "hide"):
                session["hunt_choice"] = choice
                session["hunt_finished"] = True

                frag = "HT-REVEAL" if choice == "reveal" else "HT-HIDE"
                frags = set(session.get("found_fragments", []))
                frags.add(frag)
                session["found_fragments"] = list(frags)

                session.modified = True
                return redirect(url_for("hunt_game_result"))

        return redirect(url_for("hunt_game", hid=hid))

    # GET
    if not _state_ok(state, hid):
        session.pop(HUNT_STATE_KEY, None)
        return redirect(url_for("hunt_item", hid=hid))

    labyrinth, game = eng.public_view(state)
    return render_template(
        HUNT_GAME_TEMPLATE,
        labyrinth=labyrinth,
        game=game,
        hunt_id=hid,
    )


@app.route("/hunt/result")
def hunt_game_result():
    if not is_secret():
        return redirect(url_for("inbox"))

    if not session.get("hunt_finished"):
        return redirect(url_for("hunt"))

    return render_template(
        "hunt_game_result.html",
        game={},
        choice=session.get("hunt_choice"),
    )


# ------------------------------------------------------------------
# THE PANOPTICON
# ------------------------------------------------------------------
@app.route("/panopticon")
def panopticon():
    if not is_secret():
        return redirect(url_for("inbox"))
    _remember("panopticon")
    return render_template(
        "panopticon.html",
        p=PANOPTICON,
        chats=SECRET_CHATS,
    )


@app.route("/panopticon/cam/<cam_id>", methods=["GET", "POST"])
def panopticon_cam(cam_id):
    if not is_secret():
        return redirect(url_for("inbox"))

    cam = next((c for c in PANOPTICON["cameras"] if c["id"] == cam_id), None)
    if not cam:
        return redirect(url_for("panopticon"))

    default_settings = {"bitrate": 50, "buffer": 50, "focus": 50}
    session_key = f"panopticon_{cam_id}_settings"
    current = session.get(session_key) or default_settings.copy()

    unlocked = False
    progress = 0
    error = None

    if request.method == "POST":
        current = {
            "bitrate": _int(request.form.get("bitrate"), 50),
            "buffer":  _int(request.form.get("buffer"), 50),
            "focus":   _int(request.form.get("focus"), 50),
        }
        session[session_key] = current

    # Проверка: насколько настройки близки к правильным
    correct = cam.get("settings")
    if correct:
        diffs = []
        for key in ("bitrate", "buffer", "focus"):
            val = current.get(key, 50)
            correct_val = correct.get(key, 50)
            diffs.append(abs(val - correct_val))

        max_diff = max(diffs) if diffs else 100

        # Прогресс = 0, пока разница > 20; внутри окна растёт до 100
        if max_diff > 20:
            progress = 0
        else:
            progress = int((20 - max_diff) / 20 * 100)

        if progress == 100:
            unlocked = True
            session[f"panopticon_{cam_id}_unlocked"] = True

            # фрагмент камеры → общий список
            if cam.get("fragment"):
                frags = set(session.get("found_fragments", []))
                frags.add(cam["fragment"])
                session["found_fragments"] = list(frags)

            # CAM-05: игрок увидел комнату (решение — отдельно, в /rescue)
            if cam_id == "CAM-05":
                session["panopticon_found"] = True

            session.modified = True
        else:
            unlocked = False
            session[f"panopticon_{cam_id}_unlocked"] = False

    return render_template(
        "panopticon_cam.html",
        cam=cam,
        current=current,
        unlocked=unlocked,
        progress=progress,
        error=error,
        chats=SECRET_CHATS,
    )


@app.route("/panopticon/cam/<cam_id>/rescue", methods=["POST"])
def panopticon_rescue(cam_id):
    if not is_secret():
        return redirect(url_for("inbox"))

    if cam_id != "CAM-05":
        return redirect(url_for("panopticon"))

    if not session.get(f"panopticon_{cam_id}_unlocked"):
        return redirect(url_for("panopticon_cam", cam_id=cam_id))

    # выбор делается один раз
    if not session.get("panopticon_decided"):
        choice = request.form.get("choice", "report")
        session["panopticon_decided"] = True
        session["panopticon_rescued"] = (choice == "report")
        session["panopticon_found"] = True
        session.modified = True

    return redirect(url_for("panopticon_cam_events", cam_id=cam_id))


@app.route("/panopticon/cam/<cam_id>/events")
def panopticon_cam_events(cam_id):
    if not is_secret():
        return redirect(url_for("inbox"))

    cam = next((c for c in PANOPTICON["cameras"] if c["id"] == cam_id), None)
    if not cam:
        return redirect(url_for("panopticon"))

    unlocked = session.get(f"panopticon_{cam_id}_unlocked", False)

    events = (cam.get("events_unlocked")
              if unlocked and cam.get("events_unlocked")
              else cam.get("events_normal"))

    return render_template(
        "panopticon_cam_events.html",
        cam=cam,
        events=events,
        unlocked=unlocked,
        chats=SECRET_CHATS,
    )


# ------------------------------------------------------------------
# SANITIZER
# ------------------------------------------------------------------
@app.route("/sanitizer", methods=["GET", "POST"])
def sanitizer():
    if not is_secret():
        return redirect(url_for("inbox"))

    _remember("sanitizer")

    if "san_log" not in session:
        session["san_log"] = list(SANITIZER["banner"])
        session["san_cwd"] = "/"
        session["san_wrong"] = 0
        session["san_locked"] = False

    if session.get("san_locked"):
        return render_template("sanitizer.html",
                               s=SANITIZER, output=session["san_log"],
                               locked=True, chats=SECRET_CHATS)

    if request.method == "POST":
        cmd = request.form.get("cmd", "").strip()
        out = []

        if is_suspicious_text(cmd):
            return shutdown(reason="keyword")

        parts = cmd.split()
        name = parts[0] if parts else ""
        arg = parts[1] if len(parts) > 1 else ""

        cwd = session.get("san_cwd", "/")

        def path_join(arg):
            if not arg:
                return cwd
            if arg.startswith("/"):
                return arg
            if arg in (".", "./"):
                return cwd
            if arg == "..":
                return cwd.rstrip("/").rsplit("/", 1)[0] + "/" or "/"
            return (cwd.rstrip("/") + "/" + arg).replace("//", "/")

        out.append(f"{SANITIZER['prompt']} {cmd}")

        if name == "help":
            out.append(SANITIZER["help_text"])
        elif name == "pwd":
            out.append(cwd)
        elif name == "whoami":
            out.append("anon")
        elif name == "cd":
            target = path_join(arg)
            if target in SANITIZER["fs"] or (target.rstrip("/") + "/") in SANITIZER["fs"]:
                session["san_cwd"] = target if target.endswith("/") else target + "/"
                if session["san_cwd"] == "//":
                    session["san_cwd"] = "/"
            else:
                out.append(f"cd: {target}: No such file or directory")
        elif name == "ls":
            target = path_join(arg) if arg else cwd
            key = target if target in SANITIZER["fs"] else target.rstrip("/") + "/"
            if key in SANITIZER["fs"]:
                owner, perms, content = SANITIZER["fs"][key]
                out.append(f"{perms}  {owner}  {content}")
            else:
                out.append(f"ls: {target}: No such file or directory")
        elif name == "cat":
            target = path_join(arg)
            if target == "/var/log/auth.log":
                out.append(SANITIZER["auth_log"])
            elif target in SANITIZER["fs"]:
                owner, perms, content = SANITIZER["fs"][target]
                if "r" in perms[1:4] or owner == "anon":
                    out.append(content or "[пусто]")
                else:
                    out.append(f"cat: {target}: Permission denied")
            else:
                out.append(f"cat: {target}: No such file or directory")
        elif name == "sudo" and arg == "-l":
            out.append("User anon may run the following commands:")
            out.append("  (root) NOPASSWD: /usr/bin/shred")
            out.append("  (root) NOPASSWD: /sbin/mkfs.ext4")
        elif name == "shred":
            target = path_join(arg)
            out.append(f"shred: {target}: operation not permitted")
            out.append("hint: you are not ROOT.")
        elif name == "exit":
            session["san_log"] = list(SANITIZER["banner"])
            out.append("session closed.")
        elif name == "":
            pass
        else:
            session["san_wrong"] = session.get("san_wrong", 0) + 1
            out.append(f"{name}: command not found")
            if session["san_wrong"] >= 3:
                session["san_locked"] = True
                out.append("TOO MANY FAILED COMMANDS. LOCKING IP ...")
                session["san_log"] = session["san_log"] + out
                return render_template("sanitizer.html",
                                       s=SANITIZER, output=session["san_log"],
                                       locked=True, chats=SECRET_CHATS)

        session["san_log"] = session["san_log"] + out
        session.modified = True

    return render_template("sanitizer.html",
                           s=SANITIZER, output=session["san_log"],
                           locked=False, chats=SECRET_CHATS)


# ------------------------------------------------------------------
# DEAD DROP
# ------------------------------------------------------------------
@app.route("/dead-drop", methods=["GET", "POST"])
def dead_drop():
    if not is_secret():
        return redirect(url_for("inbox"))

    _remember("dead_drop")

    # Сюжетная концовка
    plot_text = None
    hijack_role = session.get("hijack_role")
    quiz_key = session.get("quiz_key")
    motive_arch = session.get("dress_motive_arch", "use")
    if hijack_role and quiz_key:
        plot_text = _get_plot_ending(hijack_role, quiz_key, motive_arch)

    # Собираем фрагменты по session
    found = session.get("found_fragments", [])
    SOURCE_PREFIX = {
        "quiz":       "C1-17-",
        "hijack":     "04-M-",
        "catalog":    "FRAG-",
        "panopticon": "PN-",
        "hunt":       "HT-",
    }

    fragments_view = []
    for f in DEAD_DROP["fragments"]:
        src = f.get("source")
        prefix = SOURCE_PREFIX.get(src, "")
        found_val = None
        for frag in found:
            if prefix and frag.startswith(prefix):
                found_val = frag
                break
        if found_val:
            fragments_view.append({**f, "status": "FOUND", "value": found_val})
        else:
            fragments_view.append({**f, "status": "EMPTY", "value": ""})

    total = len(fragments_view)
    found_count = sum(1 for f in fragments_view if f["status"] == "FOUND")
    all_found = (total > 0 and found_count == total)

    return render_template(
        "dead_drop.html",
        d={**DEAD_DROP, "fragments": fragments_view},
        unlocked=all_found,
        error=None,
        plot_text=plot_text,
        chats=SECRET_CHATS,
        total=total,
        found_count=found_count,
    )


# ------------------------------------------------------------------
# DEBUG
# ------------------------------------------------------------------
@app.route("/debug/plot")
def debug_plot():
    if not is_secret():
        return redirect(url_for("inbox"))

    hijack_role = session.get("hijack_role")
    quiz_key = session.get("quiz_key")
    motive_arch = session.get("dress_motive_arch", "use")
    fate = FATE_BY_KEY.get(quiz_key, "held")

    if hijack_role and quiz_key:
        plot_text = _get_plot_ending(hijack_role, quiz_key, motive_arch)
    else:
        # отладка: только модификаторы, без базового финала
        mods = _plot_mods(motive_arch, fate)
        plot_text = ("(БАЗА НЕ ПРОЙДЕНА — показаны только модификаторы, "
                     f"судьба по умолчанию: {fate})\n\n" + "\n\n".join(mods))

    plot_html = (plot_text or "(пусто — пройди hijack + quiz)").replace("\n", "<br>")

    return f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>DEBUG PLOT</title>
      <style>
        body {{ background: #050607; color: #d8dee7; font-family: monospace; padding: 40px; }}
        h1 {{ color: #ff2a3d; }}
        b {{ color: #4ade80; }}
        .plot {{ margin-top: 20px; padding: 20px; border: 1px solid #4ade80; background: #0a0d12; font-size: 16px; line-height: 1.7; }}
        a {{ color: #2b6cb0; }}
        .diag {{ margin-top: 20px; padding: 14px 18px; border: 1px dashed #444; background: #0a0d12; font-size: 13px; }}
      </style>
    </head>
    <body>
      <h1>DEBUG PLOT</h1>

      <p><b>hijack_role:</b> {hijack_role or '(не пройден)'}</p>
      <p><b>quiz_key:</b> {quiz_key or '(не пройден)'}</p>
      <p><b>fate:</b> {fate}</p>
      <p><b>dress_motive_arch:</b> {motive_arch}</p>

      <div class="diag">
        <b>panopticon:</b> {_panopticon_key()}
        (found={session.get("panopticon_found")},
         decided={session.get("panopticon_decided")},
         rescued={session.get("panopticon_rescued")})<br>
        <b>hunt_choice:</b> {session.get("hunt_choice")}<br>
        <b>found_fragments:</b> {session.get("found_fragments", [])}
      </div>

      <div class="plot">
        <b>plot_text:</b><br>
        {plot_html}
      </div>

      <p style="margin-top:30px;">
        <a href="/dead-drop">→ открыть DEAD DROP</a> ·
        <a href="/reset-panopticon">→ сбросить паноптикон</a>
      </p>
    </body>
    </html>
    """


@app.route("/debug/plot-all")
def debug_plot_all():
    if not is_secret():
        return redirect(url_for("inbox"))

    roles = ["свой", "чужой", "работник", "руководство", "силовик",
             "журналист", "слабый", "милана", "мусор"]
    quiz_keys = ["aggression", "paranoia", "lies", "distrust", "isolation",
                 "existential", "selfish", "loss_of_self", "curiosity",
                 "silent", "secret_x"]

    html = ("<meta charset='utf-8'><h1>ALL PLOT ENDINGS</h1>"
            "<table border='1' cellpadding='10' "
            "style='color:#d8dee7;background:#050607;font-size:12px'>")
    html += "<tr><th>hijack \\ quiz</th>"
    for qk in quiz_keys:
        html += f"<th>{qk}<br>({FATE_BY_KEY.get(qk, '?')})</th>"
    html += "</tr>"

    for role in roles:
        html += f"<tr><td><b>{role}</b></td>"
        for qk in quiz_keys:
            text = PLOT_ENDINGS.get((role, qk)) or "— (секретная)"
            html += f"<td>{text}</td>"
        html += "</tr>"

    html += "</table>"
    return html


# ------------------------------------------------------------------
# ОТЧЁТ
# ------------------------------------------------------------------
def _normalize(text: str) -> str:
    return (text or "").strip().lower().replace("ё", "е").replace(".", "")


def _check_report(form: dict) -> tuple[dict, int]:
    """Возвращает (results, score). results[i] = True/False для каждого пункта."""
    results = {}
    score = 0

    for f in REPORT["fields"]:
        fid = f["id"]
        val = (form.get(fid) or "").strip()
        correct = f.get("correct")

        # п.11 — считаем по сессии: «сообщил» (panopticon_rescued) + «раскрыл» (hunt reveal).
        # «увидел и промолчал» и «не увидел» = 0 спасённых.
        if fid == "rescued_count":
            real = 0
            if session.get("panopticon_rescued"):
                real += 1
            if session.get("hunt_choice") == "reveal":
                real += 1
            try:
                given = int(val)
            except (TypeError, ValueError):
                given = -1
            ok = (given == real)
            results[fid] = ok
            if ok:
                score += real
            continue

        # п.1 — «жива» дороже
        if fid == "milana_status":
            ok = _normalize(val) == _normalize(f["correct"])
            results[fid] = ok
            if ok:
                score += f.get("weight", 1)
            continue

        # multi (п.3) — хотя бы одно совпадение
        if f.get("multi"):
            ok = False
            for c in correct:
                if _normalize(c) in _normalize(val):
                    ok = True
                    break
            results[fid] = ok
            if ok:
                score += 1
            continue

        # обычные
        ok = False
        for c in (correct or []):
            if _normalize(c) in _normalize(val) or _normalize(val) == _normalize(c):
                ok = True
                break
        results[fid] = ok
        if ok:
            score += 1

    return results, score


@app.route("/report", methods=["GET", "POST"])
def report():
    if not is_secret():
        return redirect(url_for("inbox"))

    _remember("report")

    # доступ только после сборки всех фрагментов
    found = session.get("found_fragments", [])
    all_found = len(found) >= 5  # 5 источников
    if not all_found:
        return redirect(url_for("dead_drop"))

    submitted = False
    results = {}
    score = 0

    if request.method == "POST":
        form = {f["id"]: request.form.get(f["id"], "") for f in REPORT["fields"]}
        session["report_form"] = form
        results, score = _check_report(form)
        session["report_results"] = results
        session["report_score"] = score
        session["report_submitted"] = True
        submitted = True
        session.modified = True

    elif session.get("report_submitted"):
        submitted = True
        results = session.get("report_results", {})
        score = session.get("report_score", 0)

    return render_template(
        "report.html",
        r=REPORT,
        submitted=submitted,
        results=results,
        score=score,
        form=session.get("report_form", {}),
        chats=SECRET_CHATS,
    )


@app.route("/report/reset")
def report_reset():
    if not is_secret():
        return redirect(url_for("inbox"))
    for k in ("report_form", "report_results", "report_score", "report_submitted"):
        session.pop(k, None)
    session.modified = True
    return redirect(url_for("report"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5009))
    app.run(host="0.0.0.0", port=port, debug=True)