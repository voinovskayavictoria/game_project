# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
from data import (
    SITE, HISTORY, TEAM, PROJECTS, OD17, TRANSFER_2021, CONSULTANT,
    HAN_INSTAGRAM, HAN_TELEGRAM, GALLERY, NEWS, PARTNERS, EXTERNAL_LINKS,
)

app = Flask(__name__)


def external_url(key):
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
        "external_url": external_url,
    }


@app.route("/")
def index():
    featured_team = [m for m in TEAM if m.get("featured")]
    active = [p for p in PROJECTS if p["status"] == "active"]
    latest = sorted(NEWS, key=lambda n: n["date"], reverse=True)[:4]
    return render_template("index.html",
                           team=featured_team, projects=active, news=latest)


@app.route("/about")
def about():
    return render_template("about.html", history=HISTORY)


@app.route("/team")
def team():
    return render_template("team.html", team=TEAM)


@app.route("/team/<slug>")
def team_member(slug):
    person = next((m for m in TEAM if m["slug"] == slug), None)
    if not person:
        abort(404)
    if slug == "han-jae-won":
        return render_template("han.html", person=person)
    return render_template("team_member.html", person=person)


@app.route("/team/han-jae-won/instagram")
def han_instagram():
    person = next(m for m in TEAM if m["slug"] == "han-jae-won")
    return render_template("social_instagram.html", person=person, feed=HAN_INSTAGRAM)


@app.route("/team/han-jae-won/telegram")
def han_telegram():
    person = next(m for m in TEAM if m["slug"] == "han-jae-won")
    return render_template("social_telegram.html", person=person, feed=HAN_TELEGRAM)


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
    if slug == "od17":
        return render_template("od17.html", od=OD17)
    return render_template("project.html", project=item)


@app.route("/od17/documents")
def od17_documents():
    return render_template("od17_documents.html", od=OD17)


@app.route("/od17/documents/transfer-2021")
def transfer_2021():
    return render_template("transfer_2021.html", doc=TRANSFER_2021, consultant=CONSULTANT)


@app.route("/od17/users")
def od17_users():
    return render_template("od17_users.html", od=OD17)


@app.route("/od17/access-control")
def access_control():
    return render_template("access_control.html", od=OD17)


@app.route("/consultant/cu")
def consultant_cu():
    return render_template("consultant.html", c=CONSULTANT)


@app.route("/gallery")
def gallery():
    return render_template("gallery.html", photos=GALLERY)


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


@app.route("/partners")
def partners():
    return render_template("partners.html")


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)