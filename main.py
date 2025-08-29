from time import perf_counter
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")


# ---------- Вспомогалки ----------
RU_MONTHS = [
    "Января","Февраля","Марта","Апреля","Мая","Июня",
    "Июля","Августа","Сентября","Октября","Ноября","Декабря"
]
RU_WEEKDAYS = [
    "Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"
]

def now_ru():
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = f"{now.day} {RU_MONTHS[now.month-1]} {now.year}"
    weekday_str = RU_WEEKDAYS[now.weekday()]
    return time_str, date_str, weekday_str

def perf_and_compression(start):
    t = perf_counter() - start
    # имитация "сжатия" как на старых движках: стабильные ~60-70%
    # берём небольшую вариацию от времени рендера
    pct = 60.0 + min(9.9, (t * 1000.0) % 10.0)
    return f"{t:0.4f}", f"{pct:0.1f}"

# Стих — НЕ МЕНЯЮ: то, что у вас уже «в норме»
POEM_LINES = [
    "Когда ночами мне одному не",
    "спится,",
    "",
    "К компьютеру душа меня зовет.",
    "",
    "За окнами на ветке спит синица,",
    "",
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

# Заглушки статистики (чтобы шаблон не падал)
STATS = dict(newbies=0, birthdays=0, regs_total=12, males=6, females=6, visits_day=0, in_chat=5)


# ---------- Маршруты ----------
@app.route("/")
def index():
    start = perf_counter()

    time_str, date_str, weekday_str = now_ru()

    ctx = {
        "header_title": "ДАВИНЧИК",
        "time_str": time_str,
        "date_str": date_str,
        "weekday_str": weekday_str,
        "poem_lines": POEM_LINES,
        "in_chat": STATS["in_chat"],
        "newbies": STATS["newbies"],
        "birthdays": STATS["birthdays"],
        "regs_total": STATS["regs_total"],
        "males": STATS["males"],
        "females": STATS["females"],
        "visits_day": STATS["visits_day"],
    }

    perf_time, compression_pct = perf_and_compression(start)
    ctx["perf_time"] = perf_time
    ctx["compression_pct"] = compression_pct

    return render_template("index.html", **ctx)


# ---------- Точка входа ----------
if __name__ == "__main__":
    # локальный запуск: python main.py
    app.run(host="0.0.0.0", port=8000, debug=False)
