from flask import Flask, render_template, request, url_for
from datetime import datetime
import pytz

app = Flask(__name__)

# ===== Стих — укладка как в 1.1 (узкая колонка, разрыв строф) =====
POEM = [
    "Когда ночами мне одному не", "спится,",
    "К компьютеру душа меня", "зовет.",
    "За окнами на ветке спит", "синица,",
    "А утром соловей там запоет.", "",
    "Письмо твое в Давинчике", "зависает,",
    "С улыбкой на лице его", "прочту,",
    "И каждый смайлик душу", "согревает,",
    "Я в сердце о тебе храню мечту!", "",
    "Рука коснется букв", "клавиатуры,",
    "И в каждом слове нежность и", "любовь,",
    "Пускай, что небеса сегодня", "хмуры,",
    "Я знаю, что напишешь ты мне", "вновь!", "",
    "Я верю, что ты будешь", "улыбаться,",
    "И верю в виртуальную любовь!!!",
    "По-разному мы можем все", "влюбляться,",
    "Но одинаково горит от страсти", "кровь..."
]

# ===== Русские месяцы/дни — стабильный вывод =====
RU_MONTHS = {
    "January":"Января","February":"Февраля","March":"Марта","April":"Апреля",
    "May":"Мая","June":"Июня","July":"Июля","August":"Августа",
    "September":"Сентября","October":"Октября","November":"Ноября","December":"Декабря",
}
RU_WEEKDAYS = {
    "Monday":"Понедельник","Tuesday":"Вторник","Wednesday":"Среда",
    "Thursday":"Четверг","Friday":"Пятница","Saturday":"Суббота","Sunday":"Воскресенье",
}

def ru_now_kyiv():
    tz = pytz.timezone("Europe/Kiev")
    now = datetime.now(tz)
    time_str = now.strftime("%H:%M:%S")
    date_str = f"{now.day} {RU_MONTHS[now.strftime('%B')]} {now.year}"
    weekday_str = RU_WEEKDAYS[now.strftime("%A")]
    return time_str, date_str, weekday_str

@app.route("/")
def index():
    time_str, date_str, weekday_str = ru_now_kyiv()
    # любые числа-заглушки — как раньше
    ctx = dict(
        header_title="ДАВИНЧИК",
        time_str=time_str, date_str=date_str, weekday_str=weekday_str,
        poem_lines=POEM,
        in_chat=5, newbies=0, birthdays=0, regs_total=12,
        males=6, females=6, visits_day=0,
        perf_time="0.0002", compression_pct="63.0"
    )
    return render_template("index.html", **ctx)

# Страница правил регистрации (без времени/даты в шапке)
@app.route("/reg")
def reg():
    stage = request.args.get("stage", "rules")
    if stage == "rules":
        return render_template("reg_rules.html", header_title="ДАВИНЧИК")
    # Можно позже доделать шаги; сейчас нужен только rules
    return render_template("reg_rules.html", header_title="ДАВИНЧИК")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
