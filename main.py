from flask import Flask, render_template, request, redirect, url_for, Response
from datetime import datetime
import locale
import time
from zoneinfo import ZoneInfo

app = Flask(__name__)

# --- Локаль и часовой пояс (Киев, русская локаль) ---
try:
    # Linux
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
except Exception:
    try:
        # Windows
        locale.setlocale(locale.LC_TIME, "Russian_Russia.1251")
    except Exception:
        pass  # если не выйдет, покажем латиницей — но маршрут не упадёт

TZ = ZoneInfo("Europe/Kyiv")

# --- Стих (замороженная версия 1.1) ---
POEM_LINES = [
    "Когда ночами мне одной не спится,",
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

def now_ru():
    dt = datetime.now(TZ)
    time_str = dt.strftime("%H:%M:%S")
    # Месяц и день недели по-русски
    date_str = dt.strftime("%d %B %Y").capitalize()
    weekday_str = dt.strftime("%A").capitalize()
    return time_str, date_str, weekday_str

@app.route("/")
def index():
    t0 = time.perf_counter()

    time_str, date_str, weekday_str = now_ru()

    # Заглушечные статистики
    stats = dict(
        in_chat=5,
        newbies=0, birthdays=0, regs_total=12,
        males=6, females=6, visits_day=0
    )

    t1 = time.perf_counter()
    perf_time = f"{t1 - t0:.4f}"
    compression_pct = "69.2"  # просто пример для вывода

    return render_template(
        "index.html",
        header_title="ДАВИНЧИК",
        time_str=time_str,
        date_str=date_str,
        weekday_str=weekday_str,
        poem_lines=POEM_LINES,
        perf_time=perf_time,
        compression_pct=compression_pct,
        **stats
    )

# --- Минимальный маршрут регистрации, чтобы кнопка «Регистрация» была рабочей ---
@app.route("/reg")
def reg():
    # ожидаем параметр stage, по умолчанию показываем «правила»
    stage = request.args.get("stage", "rules")
    if stage == "rules":
        # простая страница-заглушка «Правила регистрации»
        html = f"""
        <!doctype html><meta charset="utf-8">
        <title>Правила регистрации — ДАВИНЧИК</title>
        <style>
            body{{margin:0;font-family:"Times New Roman",serif;background:#cbd6ea}}
            .wrap{{max-width:720px;margin:12px auto;background:#eef3fb;padding:12px;border-radius:14px;
                  box-shadow: inset 0 0 0 1px #8e9db6, inset 0 0 0 4px #b5c1d6, inset 0 0 0 8px #e9eff8;}}
            .h{{text-align:center;font-weight:700;font-size:28px;color:#0a2b4f;margin:6px 0 10px}}
            .c{{text-align:center}}
            a.btn{{display:inline-block;margin-top:12px;padding:8px 16px;border:1px solid #8ea2c7;border-radius:8px;
                   background:#f2f6ff;text-decoration:none;color:#0c49b7}}
        </style>
        <div class="wrap">
          <div class="h">Правила регистрации</div>
          <div class="c">Здесь будут правила. Нажмите «Начать регистрацию», чтобы продолжить.</div>
          <div class="c"><a class="btn" href="{url_for('reg', stage='step1')}">Начать регистрацию</a></div>
          <div class="c" style="margin-top:10px"><a class="btn" href="{url_for('index')}">На главную</a></div>
        </div>
        """
        return Response(html, mimetype="text/html; charset=utf-8")
    elif stage == "step1":
        html = f"""
        <!doctype html><meta charset="utf-8">
        <title>Регистрация — шаг 1 — ДАВИНЧИК</title>
        <style>
            body{{margin:0;font-family:"Times New Roman",serif;background:#cbd6ea}}
            .wrap{{max-width:720px;margin:12px auto;background:#eef3fb;padding:12px;border-radius:14px;
                  box-shadow: inset 0 0 0 1px #8e9db6, inset 0 0 0 4px #b5c1d6, inset 0 0 0 8px #e9eff8;}}
            .h{{text-align:center;font-weight:700;font-size:24px;color:#0a2b4f;margin:6px 0 10px}}
            .c{{text-align:center}}
            a.btn{{display:inline-block;margin-top:12px;padding:8px 16px;border:1px solid #8ea2c7;border-radius:8px;
                   background:#f2f6ff;text-decoration:none;color:#0c49b7}}
        </style>
        <div class="wrap">
          <div class="h">Регистрация — шаг 1</div>
          <div class="c">Здесь будет форма ввода ника.</div>
          <div class="c"><a class="btn" href="{url_for('index')}">На главную</a></div>
        </div>
        """
        return Response(html, mimetype="text/html; charset=utf-8")
    else:
        return redirect(url_for("reg", stage="rules"))

if __name__ == "__main__":
    # Для локального запуска
    app.run(host="0.0.0.0", port=8000)
