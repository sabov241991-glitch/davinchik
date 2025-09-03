from flask import Flask, render_template
from datetime import datetime
try:
    # Предпочтительно: стандартная зона времени с автопереходом лето/зима
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Europe/Kiev")
except Exception:
    # Запасной вариант: pytz (если установлен). Тоже корректно обрабатывает DST.
    import pytz
    TZ = pytz.timezone("Europe/Kiev")

app = Flask(__name__)

# ===== Стих (укладка как на скрине — узкая колонка, переносы и строфы сохранены) =====
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
    "Но одинаково горит от страсти кровь...",
]

# Русские месяцы (родительный падеж, как в «4 Сентября 2025»)
RU_MONTHS = {
    1: "Января", 2: "Февраля", 3: "Марта", 4: "Апреля",
    5: "Мая", 6: "Июня", 7: "Июля", 8: "Августа",
    9: "Сентября", 10: "Октября", 11: "Ноября", 12: "Декабря"
}
# День недели с заглавной буквы
RU_WEEKDAYS = {
    0: "Понедельник", 1: "Вторник", 2: "Среда",
    3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"
}


@app.route("/")
def index():
    # Время Киева (с автоматическим учетом перевода часов)
    now = datetime.now(TZ)

    # Жирным — только время; дата и день недели — обычные
    time_str = now.strftime("%H:%M:%S")
    date_str = f"{now.day} {RU_MONTHS[now.month]} {now.year}"
    weekday_str = RU_WEEKDAYS[now.weekday()]

    # Остальные данные (как были)
    header_title = "ДАВИНЧИК"
    in_chat = 5
    newbies = 0
    birthdays = 0
    regs_total = 12
    males = 6
    females = 6
    visits_day = 0

    # Псевдо-метрики
    perf_time = "0.0002"
    compression_pct = "63.0"

    return render_template(
        "index.html",
        header_title=header_title,
        time_str=time_str,
        date_str=date_str,
        weekday_str=weekday_str,
        poem_lines=POEM,
        in_chat=in_chat,
        newbies=newbies,
        birthdays=birthdays,
        regs_total=regs_total,
        males=males,
        females=females,
        visits_day=visits_day,
        perf_time=perf_time,
        compression_pct=compression_pct,
    )


if __name__ == "__main__":
    # В проде Render запускает через gunicorn; локально можно так:
    app.run(host="0.0.0.0", port=5000, debug=False)
