from time import perf_counter
from datetime import datetime
from flask import Flask, render_template, render_template_string, request

app = Flask(__name__, template_folder="templates", static_folder="static")

# --------- Русские дата/время ---------
RU_MONTHS = [
    "Января","Февраля","Марта","Апреля","Мая","Июня",
    "Июля","Августа","Сентября","Октября","Ноября","Декабря"
]
RU_WEEKDAYS = [
    "Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"
]

def now_ru():
    now = datetime.now()
    return (
        now.strftime("%H:%M:%S"),
        f"{now.day} {RU_MONTHS[now.month-1]} {now.year}",
        RU_WEEKDAYS[now.weekday()],
    )

def perf_and_compression(start):
    t = perf_counter() - start
    pct = 60.0 + min(9.9, (t * 1000.0) % 10.0)
    return f"{t:0.4f}", f"{pct:0.1f}"

# --------- Данные для главной (как у тебя было) ---------
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

STATS = dict(newbies=0, birthdays=0, regs_total=12, males=6, females=6, visits_day=0, in_chat=5)

# --------- Главная ---------
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

# --------- Заглушка регистрации (чтобы ссылка не валило сайт) ---------
@app.route("/reg")
def reg():
    # stage пригодится позже (rules / step1 / step2 / done)
    stage = request.args.get("stage", "rules")
    start = perf_counter()
    perf_time, compression_pct = perf_and_compression(start)
    # Минимальная страница тем же шапочным стилем, чтобы всё работало
    return render_template_string("""
<!doctype html>
<html lang="ru"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ДАВИНЧИК — Регистрация</title>
<style>
  body{margin:0;background:linear-gradient(#cad4e5,#b8c6dc) fixed;
       font-family:"Times New Roman",Georgia,serif;color:#0a0a0a}
  .wrap{max-width:720px;margin:8px auto 20px;background:linear-gradient(#d5dff0,#d0dbed);
        border-radius:14px;padding:10px;box-shadow:
        0 0 0 1px #8e9db6 inset,0 0 0 4px #b5c1d6 inset,0 0 0 8px #e9eff8 inset,
        0 1px 0 #7f8da6,0 2px 0 #aebad0;}
  .head{ text-align:center;font-weight:700;font-size:32px;letter-spacing:1px;color:#0a2b4f;
         text-shadow:0 1px 0 #fff;margin:4px 6px 8px;padding:10px 8px;border-radius:12px;
         background:#eef3fb;box-shadow:inset 0 0 0 2px #e9eff8,inset 0 0 0 6px #fff,
         0 1px 0 #7f8da6, 0 2px 0 #aebad0;}
  .panel{background:#eef3fb;border-radius:12px;padding:12px;
         box-shadow:inset 0 0 0 2px #e9eff8, inset 0 0 0 6px #fff;}
  .center{text-align:center}
  .sep{height:1px;margin:8px 4px;background:linear-gradient(90deg,#b7c4d9,#eef3fb,#b7c4d9)}
  .btn{display:inline-block;margin-top:10px;padding:6px 14px;border:1px solid #8ea2c7;
       border-radius:8px;background:#f2f6ff;text-decoration:none;color:#0a0a0a}
  .compress{margin:10px 0 0;text-align:center;font-size:11px;line-height:1}
  .footer{margin:6px auto 6px;text-align:center;color:#22395c}
  .badge{display:inline-block;background:#fff;border:1px solid #b8c6df;border-radius:8px;
         padding:3px 6px;font-size:12px}
</style>
</head>
<body>
  <div class="wrap">
    <div class="head">ДАВИНЧИК</div>
    <div class="panel">
      <div class="center" style="font-size:24px;font-weight:700;margin:6px 0">Регистрация</div>
      <div class="center" style="color:#4a5e86;margin:6px 0">Страница «{{ stage }}» в разработке</div>
      <div class="center"><a class="btn" href="/">На главную</a></div>
    </div>
    <div class="sep"></div>
    <div class="compress">[ {{ perf_time }} | Сжатие: {{ compression_pct }}% ]</div>
    <div class="footer"><span class="badge">©ДАВИНЧИК ©2025</span></div>
  </div>
</body></html>
    """, stage=stage, perf_time=perf_time, compression_pct=compression_pct)

# --------- Точка входа ---------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
