from __future__ import annotations
import os, gzip, math, random
from datetime import datetime, timedelta, date
from time import perf_counter

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ---------- Models ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True, nullable=False)
    gender = db.Column(db.String(1), default="U")  # M / F / U
    birthday = db.Column(db.Date, nullable=True)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- Helpers ----------
RU_MONTHS = [
    "Января","Февраля","Марта","Апреля","Мая","Июня",
    "Июля","Августа","Сентября","Октября","Ноября","Декабря"
]
RU_WEEKDAYS = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

def now_ru():
    dt = datetime.now()
    time_str = dt.strftime("%H:%M:%S")
    date_str = f"{dt.day} {RU_MONTHS[dt.month-1]} {dt.year}"
    wday = RU_WEEKDAYS[dt.weekday()]
    return time_str, date_str, wday

def seed_db():
    db.create_all()
    if User.query.count() > 0:
        return
    # IDs 1..11 — системные, 12 — админ (ты)
    genders = (["M"]*6)+(["F"]*6)  # 6 парней, 6 девушек
    # распределим так, чтобы админ (id=12) был парнем
    for i in range(1,12):
        nick = f"System{i:02d}"
        g = genders[i-1]
        # День рождения — случайный, чтобы «Именинники» могли появляться
        bday = date(1990+((i*3)%15), ((i%12)+1), min(28, (i%28)+1))
        reg_at = datetime.utcnow() - timedelta(days=30+i)
        u = User(
            id=i,
            nickname=nick,
            gender=g,
            birthday=bday,
            registered_at=reg_at,
            password_hash=generate_password_hash(f"sys{i:02d}")
        )
        db.session.add(u)

    admin = User(
        id=12,
        nickname="Admin",
        gender="M",
        birthday=date(1995, 5, 20),
        registered_at=datetime.utcnow() - timedelta(days=10),
        is_admin=True,
        password_hash=generate_password_hash("123456")  # хеш пароля
    )
    db.session.add(admin)

    # Первый реальный зарегистрированный — ID13 (для будущих регистраций)
    # Сымитируем «новенького»: зарегистрирован за последние 24 часа
    newbie = User(
        id=13,
        nickname="User13",
        gender="F",
        birthday=date(1998, 8, 27),
        registered_at=datetime.utcnow() - timedelta(hours=3),
        password_hash=generate_password_hash("user13pass")
    )
    db.session.add(newbie)

    db.session.commit()

    # Обозначим 5 онлайн — обновим last_seen у 5 пользователей «прямо сейчас»
    online_ids = [1, 3, 5, 7, 12]
    now = datetime.utcnow()
    for uid in online_ids:
        u = User.query.get(uid)
        u.last_seen = now
    db.session.commit()

seed_db()

# ---------- Routes ----------
@app.route("/", methods=["GET"])
def index():
    start = perf_counter()

    # Запишем визит
    db.session.add(Visit())
    db.session.commit()

    # Данные для счётчиков
    now = datetime.utcnow()
    online_window = now - timedelta(minutes=5)
    online_count = User.query.filter(User.last_seen != None, User.last_seen > online_window).count()

    total_regs = User.query.count()  # всего регистраций
    males = User.query.filter_by(gender="M").count()
    females = User.query.filter_by(gender="F").count()

    # «Новеньких» за 24 часа
    newbies_24h = User.query.filter(User.registered_at >= now - timedelta(hours=24)).count()
    # «Именинников» сегодня (по месяцу и дню)
    today = date.today()
    birthday_count = User.query.filter(
        User.birthday != None,
        db.extract("month", User.birthday) == today.month,
        db.extract("day", User.birthday) == today.day
    ).count()

    # «Посетит. за сутки»
    visits_24h = Visit.query.filter(Visit.ts >= now - timedelta(hours=24)).count()

    # Дата/время для центрального блока
    time_str, date_str, wday = now_ru()

    # Первичный рендер (для оценки «Сжатия»)
    html_first = render_template(
        "index.html",
        header_title="ДАВИНЧИК",
        welcome_text="Добро пожаловать",
        time_str=time_str,
        date_str=date_str,
        weekday_str=wday,
        poem_lines=[
            "Когда ночами мне одной не спится,",
            "К компьютеру душа меня зовет.",
            "За окнами на ветке спит синица,",
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
        ],
        # правая колонка
        in_chat=online_count if online_count else 5,  # минимум 5 как на скрине при пустой активности
        newbies=newbies_24h,
        birthdays=birthday_count,
        regs_total=total_regs,
        males=males,
        females=females,
        partners_total=7,   # как на скрине
        visits_day=visits_24h,
        perf_time="0.0000",   # временные плейсхолдеры
        compression_pct="63.0",
    )

    # Рассчёт «Сжатия» и времени генерации
    raw = html_first.encode("utf-8")
    gz = gzip.compress(raw)
    comp_ratio = (1 - (len(gz) / max(1, len(raw)))) * 100.0
    end = perf_counter()
    elapsed = end - start

    # Финальный рендер с реальными метриками
    html_final = render_template(
        "index.html",
        header_title="ДАВИНЧИК",
        welcome_text="Добро пожаловать",
        time_str=time_str,
        date_str=date_str,
        weekday_str=wday,
        poem_lines=[
            "Когда ночами мне одной не спится,",
            "К компьютеру душа меня зовет.",
            "За окнами на ветке спит синица,",
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
        ],
        in_chat=online_count if online_count else 5,
        newbies=newbies_24h,
        birthdays=birthday_count,
        regs_total=total_regs,
        males=males,
        females=females,
        partners_total=7,
        visits_day=visits_24h,
        perf_time=f"{elapsed:.4f}",
        compression_pct=f"{comp_ratio:.1f}",
    )
    return html_final

@app.route("/login", methods=["POST"])
def login():
    nick_or_id = request.form.get("nick", "").strip()
    pwd = request.form.get("password", "")
    user = None
    if nick_or_id.isdigit():
        user = User.query.get(int(nick_or_id))
    if user is None:
        user = User.query.filter_by(nickname=nick_or_id).first()
    ok = bool(user and check_password_hash(user.password_hash, pwd))
    # Обновим last_seen при успешном «входе» (для онлайн-счётчика)
    if ok:
        user.last_seen = datetime.utcnow()
        db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Запуск: python main.py
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
