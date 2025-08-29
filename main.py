from flask import Flask, render_template, request
from datetime import datetime
import pytz, gzip, io

app = Flask(__name__)

TZ = pytz.timezone("Europe/Kyiv")

# Текст стиха (как на главной)
POEM = [
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
    "Но одинаково горит от страсти кровь...",
]

def perf_and_compression(rendered_html: str):
    # «реальное время» генерации + «сжатие»: считаем gzip-коэффициент
    start = datetime.now(TZ)
    raw = rendered_html.encode("utf-8")
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=6) as gz:
        gz.write(raw)
    comp_pct = round(100.0 * (1.0 - len(buf.getvalue()) / max(1, len(raw))), 1)
    elapsed = (datetime.now(TZ) - start).total_seconds()
    # Возвращаем строкой для шаблона
    return f"{elapsed:.4f}", comp_pct

def now_kyiv():
    dt = datetime.now(TZ)
    months = [
        "Января","Февраля","Марта","Апреля","Мая","Июня",
        "Июля","Августа","Сентября","Октября","Ноября","Декабря"
    ]
    weekdays = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
    return dt.strftime("%H:%M:%S"), f"{dt.day} {months[dt.month-1]} {dt.year}", weekdays[dt.weekday()]

@app.route("/")
def home():
    time_str, date_str, weekday_str = now_kyiv()
    html = render_template(
        "index.html",
        header_title="ДАВИНЧИК",
        time_str=time_str,
        date_str=date_str,
        weekday_str=weekday_str,
        poem_lines=POEM,
        in_chat=5, newbies=0, birthdays=0, regs_total=12, males=6, females=6, visits_day=0,
        perf_time="0", compression_pct=0
    )
    perf_time, compression_pct = perf_and_compression(html)
    return render_template(
        "index.html",
        header_title="ДАВИНЧИК",
        time_str=time_str,
        date_str=date_str,
        weekday_str=weekday_str,
        poem_lines=POEM,
        in_chat=5, newbies=0, birthdays=0, regs_total=12, males=6, females=6, visits_day=0,
        perf_time=perf_time, compression_pct=compression_pct
    )

# Новая страница «Правила регистрации»
@app.route("/register")
def register_rules():
    html = render_template("reg_rules.html", perf_time="0", compression_pct=0)
    perf_time, compression_pct = perf_and_compression(html)
    return render_template("reg_rules.html", perf_time=perf_time, compression_pct=compression_pct)

# Шаг 1: ввод ника (как было, без времени/даты)
@app.route("/register/step1", methods=["GET", "POST"])
def register_step1():
    if request.method == "POST":
        # Здесь дальше ваш шаг 2 и т.д.
        pass
    html = render_template("reg.html", perf_time="0", compression_pct=0)
    perf_time, compression_pct = perf_and_compression(html)
    return render_template("reg.html", perf_time=perf_time, compression_pct=compression_pct)

# Вход (заглушка)
@app.route("/login", methods=["POST"])
def login():
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
