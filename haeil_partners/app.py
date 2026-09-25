# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
from data import (
    SITE, TEAM, CLIENTS, PROJECTS, C17_DOCUMENTS,
    PUBLICATIONS, ARCHIVE, GALLERY, PARTNER_LINKS, EXTERNAL_LINKS,
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
        "PARTNER_LINKS": PARTNER_LINKS,
        "EXTERNAL_LINKS": EXTERNAL_LINKS,
        "external_url": external_url,
    }


@app.route("/")
def index():
    featured_team = [m for m in TEAM if m.get("featured")]
    featured_clients = [c for c in CLIENTS if c["slug"] in ("prime-systems", "vector-labs", "orbit-data")]
    return render_template(
        "index.html",
        team=featured_team,
        clients=featured_clients,
        latest_publications=PUBLICATIONS[:3],
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/team")
def team():
    return render_template("team.html", team=TEAM)


@app.route("/team/<slug>")
def team_member(slug):
    person = next((m for m in TEAM if m["slug"] == slug), None)
    if not person:
        abort(404)
    return render_template("team_member.html", person=person)


@app.route("/clients")
def clients():
    return render_template("clients.html", clients=CLIENTS)


@app.route("/clients/<slug>")
def client(slug):
    item = next((c for c in CLIENTS if c["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("client.html", client=item)


@app.route("/projects")
def projects():
    return render_template("projects.html", projects=PROJECTS)


@app.route("/projects/<slug>")
def project(slug):
    item = next((p for p in PROJECTS if p["slug"] == slug), None)
    if not item:
        abort(404)
    docs = C17_DOCUMENTS if slug == "c17" else []
    return render_template("project.html", project=item, documents=docs)


@app.route("/document/c17-transfer")
def document_c17():
    return render_template("document_c17.html")


@app.route("/publications")
def publications():
    return render_template("publications.html", publications=PUBLICATIONS)


@app.route("/publications/<slug>")
def publication(slug):
    item = next((p for p in PUBLICATIONS if p["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("publication.html", item=item)


@app.route("/archive")
def archive():
    years = sorted(ARCHIVE.keys(), reverse=True)
    current = request.args.get("year")
    return render_template("archive.html", years=years, current=current, archive=ARCHIVE)


@app.route("/gallery")
def gallery():
    return render_template("gallery.html", photos=GALLERY)


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)