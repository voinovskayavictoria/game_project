# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort
from data import SITE, TEAM, PROJECTS, NEWS, PARTNERS

app = Flask(__name__)


@app.context_processor
def inject_site():
    return {"SITE": SITE, "PARTNERS": PARTNERS}


# --- Главная ---
@app.route("/")
def index():
    latest_news = sorted(NEWS, key=lambda n: n["date"], reverse=True)[:4]
    featured = [m for m in TEAM if m.get("featured")]
    active = [p for p in PROJECTS if p["status"] == "active"]
    return render_template(
        "index.html",
        news=latest_news,
        team=featured,
        projects=active,
    )


# --- О компании ---
@app.route("/about")
def about():
    return render_template("about.html")


# --- Команда ---
@app.route("/team")
def team():
    return render_template("team.html", team=TEAM)


@app.route("/team/<slug>")
def team_member(slug):
    member = next((m for m in TEAM if m["slug"] == slug), None)
    if not member:
        abort(404)
    return render_template("team_member.html", member=member)


# --- Проекты ---
@app.route("/projects")
def projects():
    active = [p for p in PROJECTS if p["status"] == "active"]
    archived = [p for p in PROJECTS if p["status"] == "archived"]
    return render_template("projects.html", active=active, archived=archived)


@app.route("/projects/<slug>")
def project(slug):
    item = next((p for p in PROJECTS if p["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("project.html", project=item)


# --- Новости ---
@app.route("/news")
def news():
    by_year = {}
    for n in NEWS:
        year = n["date"].split(".")[-1]
        by_year.setdefault(year, []).append(n)
    by_year = dict(sorted(by_year.items(), key=lambda kv: kv[0], reverse=True))
    return render_template("news.html", by_year=by_year)


@app.route("/news/<slug>")
def news_item(slug):
    item = next((n for n in NEWS if n["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("news_item.html", item=item)


# --- Архив ---
@app.route("/archive")
def archive():
    years = ["2026", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018"]
    current = None  # можно принимать ?year= через request.args
    from flask import request
    current = request.args.get("year")
    return render_template("archive.html", years=years, current=current)


# --- Партнёры ---
@app.route("/partners")
def partners():
    return render_template("partners.html")


# --- Медиа / галерея ---
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# --- Контакты ---
@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


# --- 404 ---
@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5001)