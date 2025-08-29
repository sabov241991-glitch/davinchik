from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import locale

app = Flask(__name__)

# ----- Текст стиха: КАЖДЫЙ ЭЛЕМЕНТ — ЭТО СТРОФА -----
POEM_STANZAS = [
    """Когда ночами мне одному не спится,
К компьютеру душа меня зовет.
За окнами на ветке спит синица,
А утром соловей там запоет.""",

    """Письмо твое в Давинчике зависает,
С улыбкой на лице его прочту,
И каждый смайлик душу согревает,
Я в сердце о тебе храню мечту!""",

    """Рука коснется букв клавиатуры,
И в каждом слове нежность и любовь,
Пускай, что небеса сегодня хмуры,
Я знаю, что напишешь ты мне вновь!""",

    """Я верю, что ты будешь улыбаться,
И верю в виртуальную любовь!!!
По-разному мы можем все влюбляться,
Но одинаково горит от страсти кровь..."""
]

def ru_dt_now():
    # Дата/время по-русски (без падения, если нет ru_RU)
    try:
        locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, "ru_RU")
        except locale.Error:
            pass
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%d %B %Y")
    weekday_str = now.strftime("%A").capitalize()
    return time_str, date_str, weekday_str

@app.route("/")
def index():
    time_str, date_str, weekday_str = ru_dt_now()
    # имитация показателей «сжатия»
    perf_time = "0.0002"
    compression_pct = "69.2"
    ctx = {
        "header_title": "ДАВИНЧИК",
        "time_str": time_str,
        "date_str": date_str,
        "weekday_str": weekday_str,
        "in_chat": 5,
        "newbies": 0,
        "birthdays": 0,
        "regs_total": 12,
        "males": 6,
        "females": 6,
        "visits_day": 0,
        "perf_time": perf_time,
        "compression_pct": compression_pct,
        # ПЕРЕДАЁМ СТРОФЫ (НЕ ОТДЕЛЬНЫЕ СТРОКИ!)
        "poem_stanzas": POEM_STANZAS,
    }
    return render_template("index.html", **ctx)

# Заглушка, если у тебя уже есть свои маршруты регистрации — можешь удалить этот блок
@app.route("/reg")
def reg():
    stage = request.args.get("stage", "rules")
    return f"Регистрация ({stage}) — временная заглушка. Подключи свои шаблоны."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
