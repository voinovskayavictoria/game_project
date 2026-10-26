# -*- coding: utf-8 -*-
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    # Отдаем нашу HTML-страницу
    return render_template("osint.html")

if __name__ == "__main__":
    # Порт 5010 (свободный, чтобы не конфликтовать с другими)
    port = int(os.environ.get("PORT", 5010))
    app.run(host="0.0.0.0", port=port, debug=True)