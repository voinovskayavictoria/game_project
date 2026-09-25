# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
from data import (
    SITE, HISTORY, TEAM, PROJECTS, OD17, SYSTEM_LOG, NEWS,
    GALLERY, PARTNERS, LEGACY_MIGRATION, EXTERNAL_LINKS,
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
    active_projects = [p for p in PROJECTS if p["status"] == "active"]
    latest = NEWS[-3:][::-1]
    return render_template(
        "index.html",
        team=featured_team,
        projects=active_projects,
        news=latest,
    )


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
    return render_template("team_member.html", person=person)


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


@app.route("/od17/legacy-migration")
def legacy_migration():
    return render_template("legacy_migration.html", doc=LEGACY_MIGRATION)


@app.route("/system-log")
def system_log():
    return render_template("system_log.html", log=SYSTEM_LOG)


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
    app.run(host="0.0.0.0", port=5004, debug=True)