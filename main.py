# main.py — v1.1 (кнопка "Регистрация" с главной ведёт на /reg?stage=rules)
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import locale
import random
import time
import pytz

app = Flask(__name__)

# Локаль и часовой пояс (Киев)
try:
    # Под разные ОС
    for loc in ("ru_UA.UTF-8", "ru_UA", "ru_RU.UTF-8", "ru_RU"):
        try:
            locale.setlocale(locale.LC_TIME, loc)
            break
        except locale.Error:
            continue
except Exception:
    pass

KYIV_TZ = pytz.timezone("Europe/Kyiv")

POEM_LINES = [
    "Когда ночами мне одному не",
    "спится,",
    "К компьютеру душа меня",
    "зовет.",
    "За окнами на ветке спит",
    "синица,",
    "А утром соловей там запоет.",
    "",
    "Письмо твое в Давинчике",
    "зависает,",
    "С улыбкой на лице его",
    "прочту,",
    "И каждый смайлик душу",
    "согревает,",
    "Я в сердце о тебе храню мечту!",
    "",
    "Рука коснется букв",
    "клавиатуры,",
    "И в каждом слове нежность и",
    "любовь,",
    "Пускай, что небеса сегодня",
    "хмуры,",
    "Я знаю, что напишешь ты мне",
    "вновь!",
    "",
    "Я верю, что ты будешь",
    "улыбаться,",
    "И верю в виртуальную любовь!!!",
    "По-разному мы можем все",
    "влюбляться,",
    "Но одинаково горит от страсти",
    "кровь..."
]

def now_kyiv():
    return datetime.now(KYIV_TZ)

def fmt_date(dt: datetime):
    # «30 Августа 2025»
    return dt.strftime("%d %B %Y").capitalize()

def fmt_time(dt: datetime):
    return dt.strftime("%H:%M:%S")

def fmt_weekday(dt: datetime):
    # «Суббота»
    return dt.strftime("%A").capitalize()

def perf():
    return f"{time.perf_counter():.4f}"

def compression():
    # просто имитация процента
    return round(random.uniform(55, 72), 1)

@app.route("/")
def index():
    dt = now_kyiv()
    ctx = {
        "header_title": "ДАВИНЧИК",
        "time_str": fmt_time(dt),
        "date_str": fmt_date(dt),
        "weekday_str": fmt_weekday(dt),
        "poem_lines": POEM_LINES,
        "in_chat": 5,
        "newbies": 0,
        "birthdays": 0,
        "regs_total": 12,
        "males": 6,
        "females": 6,
        "visits_day": 0,
        "perf_time": perf(),
        "compression_pct": compression(),
    }
    return render_template("index.html", **ctx)

# -------- Регистрация (только маршрутизация) --------
@app.route("/reg")
def reg():
    """
    stage=rules  -> страница с правилами
    stage=step1  -> ввод ника (страница 1 из 2)
    stage=step2  -> ввод анкеты (страница 2 из 2)
    Сейчас рендерим только rules/step1 если шаблоны существуют у тебя в проекте.
    """
    stage = request.args.get("stage", "rules")
    if stage == "rules":
        return render_template("reg_rules.html",
                               perf_time=perf(),
                               compression_pct=compression(),
                               header_title="ДАВИНЧИК")
    elif stage == "step1":
        return render_template("reg_step1.html",
                               perf_time=perf(),
                               compression_pct=compression(),
                               header_title="ДАВИНЧИК")
    elif stage == "step2":
        return render_template("reg_step2.html",
                               perf_time=perf(),
                               compression_pct=compression(),
                               header_title="ДАВИНЧИК")
    else:
        return redirect(url_for("reg", stage="rules"))

# ---------- Логин (заглушка POST) ----------
@app.post("/login")
def login_post():
    # Здесь у тебя может быть своя логика
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
