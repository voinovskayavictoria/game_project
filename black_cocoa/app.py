# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request, redirect, url_for
from data import (
    SITE, MENU, NEWS, EVENTS, STAFF, GALLERY,
    BOOKING_CONFIRMATION, EXTERNAL_LINKS,
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
    featured = [g for g in GALLERY if g.get("featured")] or GALLERY[:1]
    latest_news = NEWS[:3]
    return render_template(
        "index.html",
        featured=featured,
        latest_news=latest_news,
        signature=MENU[0]["items"][0],
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/menu")
def menu():
    return render_template("menu.html", menu=MENU)


@app.route("/gallery")
def gallery():
    return render_template("gallery.html", photos=GALLERY)


@app.route("/news")
def news():
    return render_template("news.html", news=NEWS)


@app.route("/news/<slug>")
def news_item(slug):
    item = next((n for n in NEWS if n["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("news_item.html", item=item)


@app.route("/events")
def events():
    return render_template("events.html", events=EVENTS)


@app.route("/events/<slug>")
def event(slug):
    item = next((e for e in EVENTS if e["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("event.html", event=item)


# --- Скрытая страница: /events/1704 ---
@app.route("/events/1704")
def event_1704():
    return render_template("event_1704.html")


@app.route("/staff")
def staff():
    return render_template("staff.html", staff=STAFF)


@app.route("/map")
def map_view():
    return render_template("map.html")


@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        return redirect(url_for("booking_success"))
    return render_template("booking.html")


@app.route("/booking/confirmation")
def booking_success():
    return render_template("booking_success.html", booking=BOOKING_CONFIRMATION)


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5008, debug=True)