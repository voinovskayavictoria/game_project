# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
from data import SITE, ARCHIVE, INTERVIEWS
import os

app = Flask(__name__)

@app.context_processor
def inject_globals():
    return {"SITE": SITE}

@app.route("/")
def index():
    return render_template("index.html")

# --- Архив (список статей) ---
@app.route("/archive")
def archive():
    years = sorted(ARCHIVE.keys(), reverse=True)
    return render_template("archive.html", years=years, archive=ARCHIVE)

# --- Заглушка "Нет ключа" (сюда ведут все статьи) ---
@app.route("/archive/locked")
def locked():
    return render_template("locked.html")

# --- Интервью ---
@app.route("/interviews")
def interviews():
    return render_template("interviews.html", interviews=INTERVIEWS)

@app.route("/interviews/<slug>")
def interview(slug):
    item = next((i for i in INTERVIEWS if i["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("interview.html", item=item)

@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)