from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pytz
import time

app = Flask(__name__)

# Русские месяцы (в родительном падеже) и дни недели
RU_MONTHS = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря"
]
RU_WEEKDAYS = [
    "Понедельник", "Вторник", "Среда", "Четверг",
    "Пятница", "Суббота", "Воскресенье"
]

def now_kyiv():
    tz = pytz.timezone("Europe/Kyiv")
    return datetime.now(tz)

def ru_date_parts(dt: datetime):
    date_str = f"{dt.day:02d} {RU_MONTHS[dt.month - 1]} {dt.year}"
    weekday_str = RU_WEEKDAYS[dt.weekday()]
    time_str = dt.strftime("%H:%M:%S")
    return time_str, date_str, weekday_str

# Главная
@app.route("/")
def index():
    t0 = time.perf_counter()

    # стих (замороженная версия)
    poem_lines = [
        "Когда ночами мне одному не спится,",
        "К компьютеру душа меня зовет.",
        "За окнами на ветке спит синица,",
        "А утром соловей там запоет.",
        "",
        "Письмо твое в Давинчике зависает,",
        "С улыбкой на лице его прочту,",
        "И каждый смайлик душу согревает,",
        "Я в сердце о тебе храню мечту!",
        "",
        "Рука коснется букв клавиатуры,",
        "И в каждом слове нежность и любовь,",
        "Пускай, что небеса сегодня хмуры,",
        "Я знаю, что напишешь ты мне вновь!",
        "",
        "Я верю, что ты будешь улыбаться,",
        "И верю в виртуальную любовь!!!",
        "По-разному мы можем все влюбляться,",
        "Но одинаково горит от страсти кровь..."
    ]

    now = now_kyiv()
    time_str, date_str, weekday_str = ru_date_parts(now)

    # простая метрика «время генерации» и «сжатие»
    perf_time = f"{time.perf_counter() - t0:.4f}"
    compression_pct = "69.2"

    return render_template(
        "index.html",
        header_title="ДАВИНЧИК",
        time_str=time_str,
        date_str=date_str,
        weekday_str=weekday_str,
        poem_lines=poem_lines,
        in_chat=5,
        newbies=0,
        birthdays=0,
        regs_total=12,
        males=6,
        females=6,
        visits_day=0,
        perf_time=perf_time,
        compression_pct=compression_pct
    )

# Форма логина (заглушка, чтобы кнопка «Войти» не падала)
@app.post("/login")
def login():
    return redirect(url_for("index"))

# Заглушка для страницы регист­рации (ссылки не будут 404)
@app.route("/reg")
def reg():
    stage = request.args.get("stage", "rules")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
