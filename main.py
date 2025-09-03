from flask import Flask, render_template, request, redirect, url_for, render_template_string
from datetime import datetime
import pytz

app = Flask(__name__)

# ===== СТИХ (строки фиксированы) =====
POEM = [
    "Когда ночами мне одной не",
    "спится,",
    "К компьютеру душа меня",
    "зовет.",
    "За окнами на ветке спит",
    "синица,",
    "А утром соловей там запоет.",
    "",
    "Письмо твое в Соблазне зависает,",
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

RU_MONTHS = {
    1: "Января", 2: "Февраля", 3: "Марта", 4: "Апреля",
    5: "Мая", 6: "Июня", 7: "Июля", 8: "Августа",
    9: "Сентября", 10: "Октября", 11: "Ноября", 12: "Декабря",
}
RU_WEEKDAYS = {
    0: "Понедельник", 1: "Вторник", 2: "Среда",
    3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье",
}

@app.route("/")
def index():
    tz = pytz.timezone("Europe/Kiev")
    now = datetime.now(tz)

    time_str = now.strftime("%H:%M:%S")
    date_str = f"{now.day} {RU_MONTHS[now.month]} {now.year}"
    weekday_str = RU_WEEKDAYS[now.weekday()]

    context = dict(
        header_title="ДАВИНЧИК",
        time_str=time_str,
        date_str=date_str,
        weekday_str=weekday_str,
        poem_lines=POEM,
        in_chat=5,
        newbies=0,
        birthdays=0,
        regs_total=12,
        males=6,
        females=6,
        visits_day=0,
        perf_time="0.0002",
        compression_pct="63.0",
    )
    return render_template("index.html", **context)

@app.route("/login", methods=["POST"])
def login():
    return redirect(url_for("index"))

@app.route("/reg")
def reg():
    stage = request.args.get("stage", "rules")
    if stage == "rules":
        return render_template_string("""
<!doctype html><html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Правила регистрации</title>
<style>
  body{margin:0;background:#bfcade;font-family:"Times New Roman",serif;color:#0a0a0a}
  .wrap{max-width:720px;margin:12px auto;background:#eef3fb;border-radius:12px;
        box-shadow:inset 0 0 0 2px #e9eff8,inset 0 0 0 6px #fff;}
  .box{margin:12px;padding:12px;background:#f7f9ff;border-radius:12px;
       box-shadow:inset 0 0 0 2px #dbe5f6,inset 0 0 0 6px #ffffff;}
  h1{margin:6px 0 10px;text-align:center}
  .center{text-align:center}
  .btn{display:inline-block;padding:6px 14px;border:1px solid #8ea2c7;border-radius:8px;background:#f2f6ff;text-decoration:none;color:#0a0a0a}
</style></head><body>
<div class="wrap"><div class="box">
  <h1>Правила регистрации</h1>
  <p class="center">Здесь будут правила. Нажмите «Начать регистрацию», чтобы продолжить.</p>
  <p class="center"><a class="btn" href="{{ url_for('index') }}">На главную</a></p>
</div></div></body></html>
        """)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
