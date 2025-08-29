from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pytz, time, zlib

app = Flask(__name__)

# --------- время Киева ---------
TZ = pytz.timezone("Europe/Kyiv")

WEEKDAYS_RU = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

POEM_TEXT = [
    "Когда ночами мне одному не ",
    "спится,",
    "К компьютеру душа меня зовет.",
    "За окнами на ветке спит",
    "синица,",
    "А утром соловей там запоет.",
    "",
    "Письмо твое в Давинчике",
    "зависает,",
    "С улыбкой на лице его прочту,",
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

# --------- утилита метрик сжатия (как на главной) ---------
def render_with_metrics(template_name, **ctx):
    # 1) предварительный рендер (без метрик)
    t0 = time.perf_counter()
    provisional = render_template(template_name, **ctx, perf_time="0.0000", compression_pct="0.0")
    # 2) посчитать «сжатие»: имитация gzip через zlib
    raw = provisional.encode("utf-8")
    comp = zlib.compress(raw, level=6)
    pct = 100.0 * (1 - (len(comp) / max(1, len(raw))))
    # 3) время
    elapsed = time.perf_counter() - t0
    # 4) финальный рендер с метриками
    return render_template(template_name, **ctx,
                           perf_time=f"{elapsed:.4f}",
                           compression_pct=f"{pct:.1f}")

def now_kyiv():
    dt = datetime.now(TZ)
    time_str = dt.strftime("%H:%M:%S")
    date_str = dt.strftime("%-d %B %Y").replace("August","Августа").replace("September","Сентября")\
                                       .replace("October","Октября").replace("November","Ноября")\
                                       .replace("December","Декабря").replace("January","Января")\
                                       .replace("February","Февраля").replace("March","Марта")\
                                       .replace("April","Апреля").replace("May","Мая")\
                                       .replace("June","Июня").replace("July","Июля")
    weekday_str = WEEKDAYS_RU[dt.weekday()]
    return time_str, date_str, weekday_str

# --------- главная (как была) ---------
@app.route("/")
def index():
    time_str, date_str, weekday_str = now_kyiv()
    # системные counters (по договорённости)
    stats = dict(
        in_chat=5, newbies=0, birthdays=0, regs_total=12, males=6, females=6, visits_day=0
    )
    return render_with_metrics(
        "index.html",
        header_title="ДАВИНЧИК",
        time_str=time_str, date_str=date_str, weekday_str=weekday_str,
        poem_lines=POEM_TEXT,
        **stats
    )

# ================= РЕГИСТРАЦИЯ =================
# /reg — 3 состояния: rules, step1, step2, done
@app.route("/reg", methods=["GET", "POST"])
def reg():
    stage = request.args.get("stage", "rules")

    # общий хедер/дата-время
    time_str, date_str, weekday_str = now_kyiv()
    header = "Регистрация"

    # RULES
    if stage == "rules":
        return render_with_metrics("reg_rules.html",
                                   header_title=header,
                                   time_str=time_str, date_str=date_str, weekday_str=weekday_str)

    # STEP 1 (GET: форма, POST: редирект на step2)
    if stage == "step1":
        if request.method == "POST":
            nick = (request.form.get("nick") or "").strip()
            translit = "on" if request.form.get("translit") else "off"
            if not nick:
                # просто перерисуем, если пусто
                return render_with_metrics("reg_step1.html",
                                           header_title=header,
                                           time_str=time_str, date_str=date_str, weekday_str=weekday_str,
                                           error="Введите желаемый ник")
            return redirect(url_for("reg", stage="step2", nick=nick, t=translit))
        return render_with_metrics("reg_step1.html",
                                   header_title=header,
                                   time_str=time_str, date_str=date_str, weekday_str=weekday_str)

    # STEP 2 (Форма данных)
    if stage == "step2":
        nick = request.args.get("nick", "")
        translit = request.args.get("t", "off")
        if request.method == "POST":
            # «регистрация»
            nick = request.form.get("nick") or nick
            gender = request.form.get("gender","M")
            # простая имитация результатов
            user_id = 21420
            password = "123456"
            posts = 20000
            return redirect(url_for("reg", stage="done",
                                    nick=nick, uid=user_id, pwd=password, posts=posts))
        return render_with_metrics("reg_step2.html",
                                   header_title=header,
                                   time_str=time_str, date_str=date_str, weekday_str=weekday_str,
                                   nick=nick, translit=translit)

    # DONE
    if stage == "done":
        nick = request.args.get("nick","Гость")
        uid = request.args.get("uid","21420")
        pwd = request.args.get("pwd","123456")
        posts = request.args.get("posts","20000")
        # автологин ссылки (фиктивные)
        base = "http://davinchik.onrender.com/go.php"
        autologin_wml = f"{base}?i={uid}&p={pwd}"
        autologin_xml = f"{base}?i={uid}&p={pwd}&tpl=xml"
        return render_with_metrics("reg_done.html",
                                   header_title="Регистрация завершена",
                                   time_str=time_str, date_str=date_str, weekday_str=weekday_str,
                                   nick=nick, uid=uid, pwd=pwd, posts=posts,
                                   autologin_wml=autologin_wml, autologin_xml=autologin_xml)

    # fallback
    return redirect(url_for("reg", stage="rules"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
