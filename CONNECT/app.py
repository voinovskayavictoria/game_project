# -*- coding: utf-8 -*-
from flask import (
    Flask, render_template, request, session,
    redirect, url_for, abort,
)
from data import (
    SITE, PASSWORD_PUBLIC, PASSWORD_SECRET,
    LOGIN_PUBLIC, LOGIN_SECRET,
    PUBLIC_CHATS, SECRET_CHATS, CONTROL,
    DRESSES, DRESSES_NOTE, DRESSES_FOOTER, DRESSES_RENTAL,
    HUNT_SEASON, HUNTS, HUNT_SLOTS, HUNT_RULES_PENALTY,
    PANOPTICON, SANITIZER, DEAD_DROP,
)
import random
import datetime
import re

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-key"

CHAT_STATE = {}

ALLOWED_SKUS = {d["sku"] for d in DRESSES}


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
    CHAT_STATE.clear()
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
    """Запомнить, что чат прочитан (для текущей сессии)."""
    read = set(session.get("read_chats", []))
    read.add(chat_id)
    session["read_chats"] = list(read)
    session.modified = True


def _with_read_state(chats):
    """Вернуть копию списка чатов с обнулённым unread у прочитанных."""
    read = set(session.get("read_chats", []))
    out = []
    for c in chats:
        c2 = dict(c)
        if c2["id"] in read:
            c2["unread"] = 0
        out.append(c2)
    return out
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
    if kind == "panopticon_events":
        return panopticon_events()
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
    CHAT_STATE.clear()
    return redirect(url_for("login"))


# ------------------------------------------------------------------
# Логин
# ------------------------------------------------------------------
@app.route("/", methods=["GET"])
def root():
    if session.get("shutdown"):
        session.clear()
        CHAT_STATE.clear()
    if not is_authed():
        return redirect(url_for("login"))
    return redirect(url_for("inbox"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET" and session.get("shutdown"):
        session.clear()
        CHAT_STATE.clear()

    if request.method == "POST":
        user = request.form.get("login", "").strip().lower()
        pwd  = request.form.get("password", "").strip()

        if len(user) > 100 or len(pwd) > 100:
            return shutdown(reason="breach")

        if is_suspicious_text(pwd) and pwd not in (PASSWORD_SECRET, PASSWORD_PUBLIC):
            return shutdown(reason="keyword")

        # --- секретный вход ---
        if user == LOGIN_SECRET and pwd == PASSWORD_SECRET:
            session["authed"] = True
            session["secret"] = True
            session["fails"] = 0
            return redirect(url_for("transition"))

        # --- публичный вход ---
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
    session.clear()
    CHAT_STATE.clear()
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
    if is_secret():
        return render_template("inbox_secret.html", chats=_with_read_state(SECRET_CHATS))
    return render_template("inbox.html", chats=_with_read_state(PUBLIC_CHATS))


# ------------------------------------------------------------------
# ЧАТ — только выбор из готовых фраз
# ------------------------------------------------------------------
@app.route("/chat/<chat_id>", methods=["GET", "POST"])
def chat(chat_id):
    if not is_authed():
        return redirect(url_for("login"))

    _remember("chat", chat_id)

    if chat_id in FORBIDDEN_CHAT_IDS:
        return shutdown(reason="breach")

    # ---------- СЕКРЕТНЫЙ РАЗДЕЛ ----------
    if is_secret():
        item = _find_chat(chat_id, SECRET_CHATS)
        if not item:
            return shutdown(reason="breach")

        if request.method == "POST":
            if not item.get("writable"):
                return redirect(url_for("chat", chat_id=chat_id))

            choice_id = request.form.get("choice", "").strip()
            story = (item.get("stories") or {}).get(choice_id)
            if not story:
                return redirect(url_for("chat", chat_id=chat_id))

            now = _now_time()
            for line in story:
                CHAT_STATE.setdefault(chat_id, []).append(
                    {"from": line.get("from", "them"),
                     "text": line.get("text", ""),
                     "time": now}
                )
            return redirect(url_for("chat", chat_id=chat_id))

        _mark_read(chat_id)
        extra = CHAT_STATE.get(chat_id, [])
        return render_template(
            "chat_secret.html",
            chat=item, chats=_with_read_state(SECRET_CHATS), extra=extra,
        )

    # ---------- ПУБЛИЧНЫЙ РАЗДЕЛ ----------
    item = _find_chat(chat_id, PUBLIC_CHATS)
    if not item:
        return shutdown(reason="breach")

    if request.method == "POST":
        if not item.get("writable"):
            return redirect(url_for("chat", chat_id=chat_id))

        choice_id = request.form.get("choice", "").strip()
        story = (item.get("stories") or {}).get(choice_id)
        if not story:
            return redirect(url_for("chat", chat_id=chat_id))

        now = _now_time()
        for line in story:
            CHAT_STATE.setdefault(chat_id, []).append(
                {"from": line.get("from", "them"),
                 "text": line.get("text", ""),
                 "time": now}
            )
        return redirect(url_for("chat", chat_id=chat_id))

    _mark_read(chat_id)
    extra = CHAT_STATE.get(chat_id, [])
    return render_template(
        "chat.html",
        chat=item, chats=_with_read_state(PUBLIC_CHATS), extra=extra,
    )

    # ---------- ПУБЛИЧНЫЙ РАЗДЕЛ ----------
    item = _find_chat(chat_id, PUBLIC_CHATS)
    if not item:
        return shutdown(reason="breach")

    if request.method == "POST":
        if not item.get("writable"):
            return redirect(url_for("chat", chat_id=chat_id))

        choice_id = request.form.get("choice", "").strip()
        chosen = next(
            (c for c in item.get("choices", []) if c["id"] == choice_id),
            None,
        )
        if not chosen:
            return redirect(url_for("chat", chat_id=chat_id))

        now = _now_time()
        CHAT_STATE.setdefault(chat_id, []).append(
            {"from": "me", "text": chosen["text"], "time": now}
        )
        pool = item.get("replies", {}).get(choice_id) or ["..."]
        CHAT_STATE[chat_id].append(
            {"from": "them", "text": random.choice(pool), "time": now}
        )
        return redirect(url_for("chat", chat_id=chat_id))

    extra = CHAT_STATE.get(chat_id, [])
    return render_template(
        "chat.html",
        chat=item, chats=PUBLIC_CHATS, extra=extra,
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
    return render_template(
        "dress.html",
        dress=item,
        rental=DRESSES_RENTAL,
        chats=SECRET_CHATS,
    )


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
            "coin":    request.form.get("coin", "usdt_trc20").strip(),
        }

        for v in form.values():
            if is_suspicious_text(v):
                return shutdown(reason="keyword")

        order_id = f"ORD-{random.randint(1700, 1799)}"

        price_str = item.get("price", "")
        total = "по запросу"
        try:
            num = float(price_str.split()[0])
            hours = float(form["hours"] or 0)
            total = f"{round(num * hours, 2)} USDT"
        except Exception:
            pass

        session["shutdown"] = True
        session["shutdown_reason"] = "order"

        return render_template(
            "order_success.html",
            dress=item,
            order=form,
            order_id=order_id,
            rental=DRESSES_RENTAL,
            total=total,
            wallet=DRESSES_RENTAL["crypto"].get(form["coin"], ""),
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


# ------------------------------------------------------------------
# PANOPTICON
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


@app.route("/panopticon/events")
def panopticon_events():
    if not is_secret():
        return redirect(url_for("inbox"))
    _remember("panopticon_events")
    return render_template(
        "panopticon_events.html",
        p=PANOPTICON,
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

    unlocked = session.get("dd_unlocked", False)
    error = None

    if request.method == "POST":
        sbox = (request.form.get("sbox") or "").strip().lower()
        hsh  = (request.form.get("hash") or "").strip()

        if is_suspicious_text(sbox) or is_suspicious_text(hsh):
            return shutdown(reason="keyword")

        if sbox == DEAD_DROP["sbox_answer"] and hsh == DEAD_DROP["hash_answer"]:
            session["dd_unlocked"] = True
            unlocked = True
        else:
            error = "KEY REJECTED. INVALID S-BOX OR HASH."
            session["dd_wrong"] = session.get("dd_wrong", 0) + 1
            if session["dd_wrong"] >= 3:
                return shutdown(reason="bruteforce")

    return render_template(
        "dead_drop.html",
        d=DEAD_DROP,
        unlocked=unlocked,
        error=error,
        chats=SECRET_CHATS,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5009, debug=True)