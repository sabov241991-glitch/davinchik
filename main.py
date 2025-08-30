from flask import Flask, render_template
from datetime import datetime
import pytz

app = Flask(__name__)

# ===== Стих (как был в ранней базовой версии) =====
POEM = [
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

@app.route("/")
def index():
    # Киевское время (без дополнительных локализаций — как в 1.0)
    tz = pytz.timezone("Europe/Kiev")
    now = datetime.now(tz)
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%d %B %Y")   # Месяц будет системной локали
    weekday_str = now.strftime("%A")

    return render_template(
        "index.html",
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
        compression_pct="63.0"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
