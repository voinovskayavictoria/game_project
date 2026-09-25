# -*- coding: utf-8 -*-
from flask import (
    Flask, render_template, request, session,
    redirect, url_for, abort,
)
from data import (
    SITE, PASSWORD_PUBLIC, PASSWORD_SECRET,
    PUBLIC_CHATS, SECRET_CHATS, CONTROL,
    DRESSES, DRESSES_NOTE, DRESSES_FOOTER, DRESSES_RENTAL,
)
import random
import datetime
import re

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-key"

CHAT_STATE = {}

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


# ------------------------------------------------------------------
# Глобальная проверка. Если shutdown — редирект на /shutdown.
# Белый список: /, /login, /logout, /reset, /shutdown, статика.
# ------------------------------------------------------------------
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


# ------------------------------------------------------------------
# МАСТЕР-СБРОС (для тебя)
# ------------------------------------------------------------------
@app.route("/reset")
def reset_magic():
    """Полный сброс: чистит сессию и историю чатов. Открывай этот URL,
    чтобы после shutdown вернуться к тестированию."""
    session.clear()
    CHAT_STATE.clear()
    return redirect(url_for("login"))


# ------------------------------------------------------------------
# Логин
# ------------------------------------------------------------------
@app.route("/", methods=["GET"])
def root():
    # Любой заход на / сбрасывает shutdown — чтобы можно было перезайти
    if session.get("shutdown"):
        session.clear()
        CHAT_STATE.clear()
    if not is_authed():
        return redirect(url_for("login"))
    return redirect(url_for("inbox"))


@app.route("/login", methods=["GET", "POST"])
def login():
    # GET /login всегда сбрасывает shutdown — мастер-вход
    if request.method == "GET" and session.get("shutdown"):
        session.clear()
        CHAT_STATE.clear()

    if request.method == "POST":
        pwd = request.form.get("password", "").strip()

        if len(pwd) > 100:
            return shutdown(reason="breach")

        if is_suspicious_text(pwd) and pwd not in (PASSWORD_SECRET, PASSWORD_PUBLIC):
            return shutdown(reason="keyword")

        if pwd == PASSWORD_SECRET:
            session["authed"] = True
            session["secret"] = True
            session["fails"] = 0
            return redirect(url_for("transition"))

        if pwd == PASSWORD_PUBLIC:
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
    if is_secret():
        return render_template("inbox_secret.html", chats=SECRET_CHATS)
    return render_template("inbox.html", chats=PUBLIC_CHATS)


# ------------------------------------------------------------------
# Чат
# ------------------------------------------------------------------
@app.route("/chat/<chat_id>", methods=["GET", "POST"])
def chat(chat_id):
    if not is_authed():
        return redirect(url_for("login"))

    if chat_id in FORBIDDEN_CHAT_IDS:
        return shutdown(reason="breach")

    if is_secret():
        item = _find_chat(chat_id, SECRET_CHATS)
        if not item:
            return shutdown(reason="breach")

        if request.method == "POST":
            text = request.form.get("text", "").strip()
            if is_suspicious_text(text):
                return shutdown(reason="keyword")
            if text:
                now = _now_time()
                CHAT_STATE.setdefault(chat_id, []).append(
                    {"from": "me", "text": text, "time": now}
                )
            return redirect(url_for("chat", chat_id=chat_id))

        extra = CHAT_STATE.get(chat_id, [])
        return render_template(
            "chat_secret.html",
            chat=item, chats=SECRET_CHATS, extra=extra,
        )

    item = _find_chat(chat_id, PUBLIC_CHATS)
    if not item:
        return shutdown(reason="breach")

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if is_suspicious_text(text):
            return shutdown(reason="keyword")
        if text:
            now = _now_time()
            CHAT_STATE.setdefault(chat_id, []).append(
                {"from": "me", "text": text, "time": now}
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

    if not re.fullmatch(r"DR-17(0[1-9]|[1-4][0-9]|50)", sku):
        return shutdown(reason="breach")

    item = next((d for d in DRESSES if d["sku"] == sku), None)
    if not item:
        return shutdown(reason="breach")

    return render_template(
        "dress.html",
        dress=item,
        rental=DRESSES_RENTAL,
        chats=SECRET_CHATS,
    )


# ------------------------------------------------------------------
# Заказ
# ------------------------------------------------------------------
@app.route("/catalog/<sku>/order", methods=["GET", "POST"])
def order(sku):
    if not is_secret():
        return redirect(url_for("inbox"))

    if not re.fullmatch(r"DR-17(0[1-9]|[1-4][0-9]|50)", sku):
        return shutdown(reason="breach")

    item = next((d for d in DRESSES if d["sku"] == sku), None)
    if not item:
        return shutdown(reason="breach")

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


# ------------------------------------------------------------------
# Shutdown
# ------------------------------------------------------------------
@app.route("/shutdown")
def shutdown_page():
    reason = request.args.get("reason") or session.get("shutdown_reason") or "breach"
    session["shutdown"] = True
    session["shutdown_reason"] = reason
    return render_template("shutdown.html", reason=reason)


# ------------------------------------------------------------------
# Control
# ------------------------------------------------------------------
@app.route("/control")
def control():
    if not is_secret():
        return shutdown(reason="breach")
    return render_template("control.html", control=CONTROL, chats=SECRET_CHATS)


# ------------------------------------------------------------------
# 404
# ------------------------------------------------------------------
@app.errorhandler(404)
def not_found(_e):
    path = (request.path or "").lower()
    for p in SUSPICIOUS_PATHS:
        if path.startswith(p):
            return shutdown(reason="breach")
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5009, debug=True)