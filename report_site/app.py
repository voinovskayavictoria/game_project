# -*- coding: utf-8 -*-
"""
Отдельный сайт «Отчёт агентства». Не зависит от основной игры.
Запуск:  python app.py      (порт 5011, поменять: PORT=5012 python app.py)
Ссылка на основную игру в кнопке «назад»: MAIN_URL=http://localhost:5009
"""
import os
import re
from difflib import SequenceMatcher

from flask import Flask, render_template, request, redirect, url_for
from jinja2 import ChoiceLoader, FileSystemLoader

from report_data import REPORT, RESCUE_OPTIONS, RESCUE_VERDICT

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
# ищем report.html и в templates/, и просто рядом с app.py
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(BASE, "templates")),
    FileSystemLoader(BASE),
])

MAIN_URL = os.environ.get("MAIN_URL", "")


def _norm(text):
    """нижний регистр, ё→е, без пробелов и знаков препинания"""
    t = (text or "").lower().replace("ё", "е")
    return re.sub(r"[\W_]+", "", t, flags=re.UNICODE)


def _match(val, correct_list, fuzzy=True):
    """совпадение с допуском на опечатки (Ordit Data, проститутции и т.п.)"""
    v = _norm(val)
    if not v:
        return False
    tokens = [_norm(t) for t in re.findall(r"\w+", (val or "").lower().replace("ё", "е"))]
    for c in correct_list:
        c = _norm(c)
        if not c:
            continue
        if v == c:
            return True
        if len(c) > 3 and c in v:     # короткие шаблоны — только точное совпадение
            return True
        if fuzzy and len(c) >= 5:
            if SequenceMatcher(None, v, c).ratio() >= 0.8:
                return True
            for t in tokens:
                if len(t) >= 5 and SequenceMatcher(None, t, c).ratio() >= 0.8:
                    return True
    return False


def _check(values):
    """results[id] = True/False только для оцениваемых полей; score; max_score"""
    results, score, max_score = {}, 0, 0
    for f in REPORT["fields"]:
        t = f["type"]
        if t == "text":
            max_score += 1
            ok = _match(values.get(f["id"], ""), f["correct"], f.get("fuzzy", True))
            results[f["id"]] = ok
            score += ok
        elif t == "multi":
            max_score += 1
            raw = _norm(values.get(f["id"], ""))
            canon = {"admin": ("admin01",), "belyakov": ("беляков", "belyakov"),
                     "melnikov": ("мельников", "melnikov")}
            found = {k for k, variants in canon.items() if any(v in raw for v in variants)}
            ok = len(found) >= f.get("need", 1)
            results[f["id"]] = ok
            score += ok
    return results, score, max_score


@app.route("/", methods=["GET", "POST"])
def report():
    submitted = False
    results, score, max_score = {}, 0, 0
    values = {}
    rescued_count = 0

    max_score = sum(1 for f in REPORT["fields"] if f["type"] in ("text", "multi"))

    if request.method == "POST":
        for f in REPORT["fields"]:
            if f["type"] == "check":
                picked = [o for o in request.form.getlist(f["id"]) if o in RESCUE_OPTIONS]
                values[f["id"]] = picked
            elif f["type"] == "select":
                v = request.form.get(f["id"], "")
                values[f["id"]] = v if v in f["options"] else ""
            else:
                values[f["id"]] = request.form.get(f["id"], "").strip()[:200]
        values["_investigator"] = request.form.get("_investigator", "").strip()[:60]

        results, score, max_score = _check(values)
        rescued_count = len(values.get("rescued", []))
        submitted = True

    pct = round(score / max_score * 100) if max_score else 0
    if pct >= 85:
        verdict = "Отчёт принят. Выводы подтверждены материалами дела."
    elif pct >= 50:
        verdict = "Отчёт принят частично. Часть выводов требует уточнения."
    else:
        verdict = "Отчёт отклонён. Слишком много расхождений с материалами дела."

    return render_template(
        "agency_report.html",
        r=REPORT,
        submitted=submitted,
        results=results,
        score=score,
        max_score=max_score,
        verdict=verdict,
        values=values,
        rescued_count=rescued_count,
        rescue_verdict=RESCUE_VERDICT.get(rescued_count, ""),
        main_url=MAIN_URL,
    )


@app.route("/reset")
def reset():
    return redirect(url_for("report"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5011))
    app.run(host="0.0.0.0", port=port, debug=True)