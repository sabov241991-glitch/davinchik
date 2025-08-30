from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from zoneinfo import ZoneInfo
import time

app = Flask(__name__)

# ===== РУССКАЯ ДАТА ДЛЯ КИЕВА =====
RU_MONTHS = {
    1: "Января", 2: "Февраля", 3: "Марта", 4: "Апреля",
    5: "Мая", 6: "Июня", 7: "Июля", 8: "Августа",
    9: "Сентября", 10: "Октября", 11: "Ноября", 12: "Декабря"
}
RU_WEEKDAYS = {
    0: "Понедельник", 1: "Вторник", 2: "Среда",
    3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"
}

def ru_datetime_kyiv():
    now = datetime.now(ZoneInfo("Europe/Kyiv"))
    time_str = now.strftime("%H:%M:%S")
    date_str = f"{now.day} {RU_MONTHS[now.month]} {now.year}"
    weekday_str = RU_WEEKDAYS[now.weekday()]
    return time_str, date_str, weekday_str

# ===== ТЕКСТ СТИХА (как в версии 1.1) =====
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

# ===== Метрики для «Сжатие» =====
def perf_info(start):
    dt = time.perf_counter() - start
    # простая «оценка сжатия» как декоративный параметр
    compression = 60.0 + (time.time() % 10)  # ~60–69%
    return f"{dt:.4f}", f"{compression:.1f}"

@app.route("/")
def index():
    t0 = time.perf_counter()
    time_str, date_str, weekday_str = ru_datetime_kyiv()
    perf_time, compression_pct = perf_info(t0)

    # демоданные справа
    stats = dict(
        newbies=0, birthdays=0, regs_total=12,
        males=6, females=6, visits_day=0, in_chat=5
    )

    return render_template(
        "index.html",
        header_title="ДАВИНЧИК",
        time_str=time_str,
        date_str=date_str,
        weekday_str=weekday_str,
        poem_lines=POEM,
        perf_time=perf_time,
        compression_pct=compression_pct,
        **stats
    )

# ===== РЕГИСТРАЦИЯ =====
@app.route("/reg")
def reg():
    # по умолчанию – страница «Правила регистрации»
    stage = request.args.get("stage", "rules")
    t0 = time.perf_counter()
    perf_time, compression_pct = perf_info(t0)

    if stage == "rules":
        return render_template(
            "reg_rules.html",
            header_title="ДАВИНЧИК",
            perf_time=perf_time,
            compression_pct=compression_pct
        )
    elif stage == "nick":  # следующий шаг (пока просто заглушка-редирект на rules)
        return redirect(url_for("reg", stage="rules"))
    else:
        return redirect(url_for("reg", stage="rules"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
