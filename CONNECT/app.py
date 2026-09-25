# -*- coding: utf-8 -*-
from flask import (
    Flask, render_template, request, session,
    redirect, url_for, abort,
)
from data import (
    SITE, PASSWORD_PUBLIC, PASSWORD_SECRET,
    PUBLIC_CHATS, SECRET_CHATS, CONTROL,
)

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-key"


# ------------------------------------------------------------------
# Вспомогательные
# ------------------------------------------------------------------
def is_authed():
    return session.get("authed", False)

def is_secret():
    return session.get("secret", False)


# ------------------------------------------------------------------
# Логин
# ------------------------------------------------------------------
@app.route("/", methods=["GET"])
def root():
    if not is_authed():
        return redirect(url_for("login"))
    return redirect(url_for("inbox"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pwd = request.form.get("password", "").strip()

        # --- секретный пароль ---
        if pwd == PASSWORD_SECRET:
            session["authed"] = True
            session["secret"] = True
            return redirect(url_for("transition"))

        # --- обычный пароль ---
        if pwd == PASSWORD_PUBLIC:
            session["authed"] = True
            session["secret"] = False
            return redirect(url_for("inbox"))

        # --- неверный ---
        return render_template("login.html", error=True)

    return render_template("login.html", error=False)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ------------------------------------------------------------------
# Переходный экран (после секретного пароля)
# ------------------------------------------------------------------
@app.route("/transition")
def transition():
    if not is_secret():
        return redirect(url_for("inbox"))
    return render_template("transition.html")


# ------------------------------------------------------------------
# Публичная часть
# ------------------------------------------------------------------
@app.route("/inbox")
def inbox():
    if not is_authed():
        return redirect(url_for("login"))

    if is_secret():
        return render_template(
            "inbox_secret.html",
            chats=SECRET_CHATS,
            site=SITE,
        )

    return render_template(
        "inbox.html",
        chats=PUBLIC_CHATS,
        site=SITE,
    )


@app.route("/chat/<chat_id>")
def chat(chat_id):
    if not is_authed():
        return redirect(url_for("login"))

    # --- секретный чат ---
    if is_secret():
        item = next((c for c in SECRET_CHATS if c["id"] == chat_id), None)
        if not item:
            abort(404)
        return render_template(
            "chat_secret.html",
            chat=item,
            chats=SECRET_CHATS,
            site=SITE,
        )

    # --- публичный чат ---
    item = next((c for c in PUBLIC_CHATS if c["id"] == chat_id), None)
    if not item:
        abort(404)
    return render_template(
        "chat.html",
        chat=item,
        chats=PUBLIC_CHATS,
        site=SITE,
    )


# ------------------------------------------------------------------
# Панель управления (только под секретным паролем)
# ------------------------------------------------------------------
@app.route("/control")
def control():
    if not is_secret():
        return redirect(url_for("inbox"))
    return render_template(
        "control.html",
        control=CONTROL,
        chats=SECRET_CHATS,
        site=SITE,
    )


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5009, debug=True)