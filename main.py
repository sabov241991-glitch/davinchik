import time
import zlib
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, render_template, request, redirect, url_for, Response

app = Flask(__name__)

# --------- Утилита рендера с метриками (время + "сжатие") ----------
def render_with_metrics(tpl_name: str, **ctx) -> Response:
    """Рендерим шаблон и добавляем метрики, как на главной."""
    # 1-й проход — нужен, чтобы посчитать "сжатие" по фактическому HTML
    t0 = time.perf_counter()
    html1 = render_template(tpl_name, **ctx)
    elapsed = time.perf_counter() - t0

    raw = html1.encode("utf-8")
    comp = zlib.compress(raw, 6)
    # % экономии (как и раньше показывали)
    try:
        saving_pct = (1 - len(comp) / max(len(raw), 1)) * 100.0
    except Exception:
        saving_pct = 0.0

    # 2-й проход — отрисуем уже с метриками
    ctx2 = dict(ctx)
    ctx2["perf_time"] = f"{elapsed:0.4f}"
    ctx2["compression_pct"] = f"{saving_pct:0.1f}"
    html2 = render_template(tpl_name, **ctx2)
    return Response(html2, mimetype="text/html; charset=utf-8")


# --------- Данные для главной (поэма и статусы) ----------
POEM_LINES = [
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

def now_kyiv():
    dt = datetime.now(ZoneInfo("Europe/Kyiv"))
    return {
        "time_str": dt.strftime("%H:%M:%S"),
        "date_str": dt.strftime("%d %B %Y"),
        "weekday_str": dt.strftime("%A"),
    }


@app.route("/")
def index():
    t = now_kyiv()
    ctx = {
        "header_title": "ДАВИНЧИК",
        "time_str": t["time_str"],
        "date_str": t["date_str"],
        "weekday_str": t["weekday_str"],
        "poem_lines": POEM_LINES,
        # счётчики, как ты просил
        "in_chat": 5,
        "newbies": 0,
        "birthdays": 0,
        "regs_total": 12,
        "males": 6,
        "females": 6,
        "visits_day": 0,
        # заглушки метрик — реальные значения подставит render_with_metrics
        "perf_time": "0.0000",
        "compression_pct": "0.0",
    }
    return render_with_metrics("index.html", **ctx)


# --------- Регистрация (все стадии через один маршрут /reg) ----------
@app.route("/reg", methods=["GET", "POST"])
def reg():
    stage = request.args.get("stage", "rules")

    # Правила (скрин 1)
    if stage == "rules":
        t = now_kyiv()
        return render_with_metrics(
            "reg.html",
            stage="rules",
            header_title="ДАВИНЧИК",
            **t,
            perf_time="0.0000",
            compression_pct="0.0",
        )

    # Шаг 1 (скрин 2)
    if stage == "step1":
        if request.method == "POST":
            nick = request.form.get("nick", "").strip()
            translit = "on" if request.form.get("translit") else "off"
            # Ник "свободен" → переходим на шаг 2
            return redirect(url_for("reg", stage="step2", nick=nick, tr=translit))
        t = now_kyiv()
        return render_with_metrics(
            "reg.html",
            stage="step1",
            header_title="ДАВИНЧИК",
            **t,
            perf_time="0.0000",
            compression_pct="0.0",
        )

    # Шаг 2 (скрин 3)
    if stage == "step2":
        nick = request.args.get("nick", "User")
        if request.method == "POST":
            # Тут могла бы быть настоящая проверка и создание,
            # но для статической демонстрации сразу "успех":
            usr_id = 21420
            pwd = "123456"
            return redirect(
                url_for("reg", stage="done", nick=nick, user_id=usr_id, pwd=pwd)
            )

        t = now_kyiv()
        return render_with_metrics(
            "reg.html",
            stage="step2",
            header_title="ДАВИНЧИК",
            nick=nick,
            **t,
            perf_time="0.0000",
            compression_pct="0.0",
        )

    # Завершение (скрин 4)
    if stage == "done":
        nick = request.args.get("nick", "User")
        user_id = request.args.get("user_id", "21420")
        pwd = request.args.get("pwd", "123456")
        # Псевдо-ссылки «автологина» как на скрине
        base = "http://davinchik.onrender.com/go.php"
        autologin_plain = f"{base}?i={user_id}&p={pwd}"
        autologin_xml = f"{base}?i={user_id}&p={pwd}&tpl=xml"
        t = now_kyiv()
        return render_with_metrics(
            "reg.html",
            stage="done",
            header_title="ДАВИНЧИК",
            nick=nick,
            user_id=user_id,
            pwd=pwd,
            autologin_plain=autologin_plain,
            autologin_xml=autologin_xml,
            **t,
            perf_time="0.0000",
            compression_pct="0.0",
        )

    # На всякий случай — если передан кривой stage
    return redirect(url_for("reg", stage="rules"))


if __name__ == "__main__":
    # Локальный запуск
    app.run(host="0.0.0.0", port=5000)
