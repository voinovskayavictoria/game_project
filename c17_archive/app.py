# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
from data import (
    SITE, EXTERNAL_LINKS, PROJECT, USERS, ACCESS_LOG, CHANGELOG,
    FILES, SYSTEM_LOG, DELETED_RECORDS, CU_PROFILE,
    ARCHIVED_DATA, PRIVATE_NODE,
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
        "EXTERNAL_LINKS": EXTERNAL_LINKS,
        "external_url": external_url,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/project")
def project():
    return render_template("project.html", project=PROJECT)


@app.route("/users")
def users():
    return render_template("users.html", users=USERS)


@app.route("/users/<user_id>")
def user_detail(user_id):
    person = next((u for u in USERS if u["id"] == user_id), None)
    if not person:
        abort(404)
    return render_template("user_detail.html", person=person)


@app.route("/access-log")
def access_log():
    return render_template("access_log.html", log=ACCESS_LOG)


@app.route("/changelog")
def changelog():
    return render_template("changelog.html", changelog=CHANGELOG)


@app.route("/files")
def files():
    return render_template("files.html", files=FILES)


@app.route("/files/<file_id>")
def file_detail(file_id):
    item = next((f for f in FILES if f["id"] == file_id), None)
    if not item:
        abort(404)

    # --- Особые страницы ---
    if item.get("special") == "transfer":
        return render_template("file_detail.html", file=item, transfer=True)
    if item.get("special") == "cu":
        return render_template("cu.html", cu=CU_PROFILE)
    if item.get("special") == "photo":
        return render_template("photo_1704.html")

    return render_template("file_detail.html", file=item)


@app.route("/system-log")
def system_log():
    return render_template("system_log.html", log=SYSTEM_LOG)


@app.route("/deleted")
def deleted():
    return render_template("deleted.html", records=DELETED_RECORDS)


@app.route("/cu")
def cu():
    return render_template("cu.html", cu=CU_PROFILE)


@app.route("/archive")
def archived_data():
    years = sorted(ARCHIVED_DATA.keys(), reverse=True)
    return render_template("archived_data.html", years=years, data=ARCHIVED_DATA)


@app.route("/archive/<year>")
def archive_year(year):
    item = ARCHIVED_DATA.get(year)
    if not item:
        abort(404)
    return render_template("archive_year.html", year=year, item=item)


# --- Скрытая страница ---
@app.route("/archive/c17/1704")
def private_node():
    return render_template("private_node.html", node=PRIVATE_NODE)


# --- 404 ---
@app.errorhandler(404)
def not_found(_e):
    return render_template("lost.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)