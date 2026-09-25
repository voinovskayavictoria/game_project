# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
from data import (
    SITE, BIO, INVESTIGATIONS, DOCUMENTS, SOURCES,
    TIMELINE, INCONSISTENCIES, CONNECT_PARTS, EXTERNAL_LINKS,
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
        "BIO": BIO,
        "EXTERNAL_LINKS": EXTERNAL_LINKS,
        "external_url": external_url,
    }


@app.route("/")
def index():
    latest = INVESTIGATIONS[0]   # connect
    others = INVESTIGATIONS[1:4]
    return render_template("index.html", latest=latest, others=others)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/investigations")
def investigations():
    return render_template("investigations.html", items=INVESTIGATIONS)


@app.route("/investigations/<slug>")
def investigation(slug):
    if slug == "connect":
        return render_template("connect.html", parts=CONNECT_PARTS)
    item = next((i for i in INVESTIGATIONS if i["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("investigation.html", item=item)


@app.route("/documents")
def documents():
    return render_template("documents.html", documents=DOCUMENTS)


@app.route("/documents/<doc_id>")
def document(doc_id):
    item = next((d for d in DOCUMENTS if d["id"] == doc_id), None)
    if not item:
        abort(404)
    return render_template("document.html", doc=item)


@app.route("/sources")
def sources():
    return render_template("sources.html", sources=SOURCES)


@app.route("/timeline")
def timeline():
    return render_template("timeline.html", timeline=TIMELINE)


@app.route("/inconsistencies")
def inconsistencies():
    return render_template("inconsistencies.html", items=INCONSISTENCIES)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    sent = False
    if request.method == "POST":
        # сюда потом повесишь реальную логику — сохранение в файл,
        # отправку на почту, и т.д.
        sent = True
    return render_template("contact.html", sent=sent)


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007, debug=True)