# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
from data import (
    SITE, PARTICIPANTS, SPEAKERS, PROGRAM, GALLERY, NEWS,
    PARTNERS, EXTERNAL_LINKS,
)

app = Flask(__name__)


def build_external_url(key):
    """Строит ссылку на другой сайт игры с учётом текущего хоста."""
    info = EXTERNAL_LINKS.get(key)
    if not info:
        return "#"
    host = request.host.split(":")[0]
    scheme = request.scheme
    return f"{scheme}://{host}:{info['port']}/"


@app.context_processor
def inject_globals():
    return {
        "SITE": SITE,
        "PARTNERS": PARTNERS,
        "EXTERNAL_LINKS": EXTERNAL_LINKS,
        "external_url": build_external_url,
    }


# --- Главная ---
@app.route("/")
def index():
    latest = sorted(NEWS, key=lambda n: n["date"], reverse=True)[:4]
    featured_participants = [p for p in PARTICIPANTS if p.get("featured")]
    featured_photos = [g for g in GALLERY if g.get("featured")]
    upcoming = PROGRAM.get(2026)
    return render_template(
        "index.html",
        news=latest,
        participants=featured_participants,
        photos=featured_photos,
        upcoming=upcoming,
    )


# --- О форуме ---
@app.route("/about")
def about():
    return render_template("about.html")


# --- Участники ---
@app.route("/participants")
def participants():
    return render_template("participants.html", participants=PARTICIPANTS)


@app.route("/participants/<slug>")
def participant(slug):
    person = next((p for p in PARTICIPANTS if p["slug"] == slug), None)
    if not person:
        abort(404)
    return render_template("participant.html", person=person)


# --- Спикеры ---
@app.route("/speakers")
def speakers():
    return render_template("speakers.html", speakers=SPEAKERS)


# --- Программа ---
@app.route("/program")
def program():
    years = sorted(PROGRAM.keys(), reverse=True)
    return render_template("program.html", years=years, program=PROGRAM)


@app.route("/program/<int:year>")
def program_year(year):
    item = PROGRAM.get(year)
    if not item:
        abort(404)
    return render_template("program_year.html", year=year, item=item)


# --- Галерея ---
@app.route("/gallery")
def gallery():
    by_year = {}
    for g in GALLERY:
        by_year.setdefault(g["year"], []).append(g)
    by_year = dict(sorted(by_year.items(), key=lambda kv: kv[0], reverse=True))
    return render_template("gallery.html", by_year=by_year)


# --- Партнёры ---
@app.route("/partners")
def partners():
    return render_template("partners.html")


# --- Новости ---
@app.route("/news")
def news():
    items = sorted(NEWS, key=lambda n: n["date"], reverse=True)
    return render_template("news.html", news=items)


@app.route("/news/<slug>")
def news_item(slug):
    item = next((n for n in NEWS if n["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("news_item.html", item=item)


# --- Архив ---
@app.route("/archive")
def archive():
    years = sorted(PROGRAM.keys(), reverse=True)
    current = request.args.get("year", type=int)
    return render_template("archive.html", years=years, current=current, program=PROGRAM)


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)