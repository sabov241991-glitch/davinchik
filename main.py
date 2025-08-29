from flask import Flask, render_template, request
from datetime import datetime
import pytz

app = Flask(__name__)

# ===== Стих строфами =====
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

# ===== Киевское время + русские месяцы/дни =====
RU_MONTHS = [
    "Января","Февраля","Марта","Апреля","Мая","Июня",
    "Июля","Августа","Сентября","Октября","Ноября","Декабря"
]
RU_WEEKDAYS = [
    "Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"
]

def now_kyiv():
    tz = pytz.timezone("Europe/Kyiv")
    dt = datetime.now(tz)
    time_str = dt.strftime("%H:%M:%S")
    date_str = f"{dt.day} {RU_MONTHS[dt.month-1]} {dt.year}"
    weekday_str = RU_WEEKDAYS[dt.weekday()]
    return time_str, date_str, weekday_str

# ===== Заглушка статистики =====
STATS = dict(newbies=0, birthdays=0, regs_total=12, males=6, females=6, visits_day=0, in_chat=5)

@app.route("/")
def index():
    time_str, date_str, weekday_str = now_kyiv()

    # имитация показателей «сжатия»
    perf_time = "0.0002"
    compression_pct = "69.2"

    ctx = {
        "header_title": "ДАВИНЧИК",
        "time_str": time_str,
        "date_str": date_str,
        "weekday_str": weekday_str,
        "in_chat": STATS["in_chat"],
        "newbies": STATS["newbies"],
        "birthdays": STATS["birthdays"],
        "regs_total": STATS["regs_total"],
        "males": STATS["males"],
        "females": STATS["females"],
        "visits_day": STATS["visits_day"],
        "perf_time": perf_time,
        "compression_pct": compression_pct,
        "poem_stanzas": POEM_STANZAS,
    }
    return render_template("index.html", **ctx)

# ===== Заглушка регистрации =====
@app.route("/reg")
def reg():
    stage = request.args.get("stage", "rules")
    return f"Регистрация ({stage}) — временно в разработке."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
