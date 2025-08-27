from __future__ import annotations
import os, gzip
from pathlib import Path
from datetime import datetime, timedelta, date
from time import perf_counter

from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# === Flask ===
app = Flask(__name__)
BASEDIR = Path(__file__).resolve().parent
DB_PATH = BASEDIR / "chat.db"

# === SQLAlchemy (SQLite-файл в рабочей папке Render) ===
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# === Models ===
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True, nullable=False)
    gender = db.Column(db.String(1), default="U")  # M/F/U
    birthday = db.Column(db.Date, nullable=True)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, default=datetime.utcnow)

# === RU date helpers ===
RU_MONTHS = [
    "Января","Февраля","Марта","Апреля","Мая","Июня",
    "Июля","Августа","Сентября","Октября","Ноября","Декабря"
]
RU_WEEKDAYS = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

def now_ru():
    dt = datetime.now()
    return dt.strftime("%H:%M:%S"), f"{dt.day} {RU_MONTHS[dt.month-1]} {dt.year}", RU_WEEKDAYS[dt.weekday()]

# === Seed ===
def seed_db():
    if User.query.count() > 0:
        return
    # ID1..11 — системные; ID12 — Admin; ID13 — первый обычный
    genders = (["M"]*6)+(["F"]*6)
    for i in range(1,12):
        u = User(
            id=i,
            nickname=f"System{i:02d}",
            gender=genders[i-1],
            birthday=date(1990 + (i % 10), ((i % 12) + 1), min(28, (i % 28) + 1)),
            registered_at=datetime.utcnow() - timedelta(days=30+i),
            password_hash=generate_password_hash(f"sys{i:02d}")
        )
        db.session.add(u)

    admin = User(
        id=12, nickname="Admin", gender="M",
        birthday=date(1995,5,20),
        registered_at=datetime.utcnow() - timedelta(days=10),
        is_admin=True,
        password_hash=generate_password_hash("123456")  # пароль захеширован
    )
    newbie = User(
        id=13, nickname="User13", gender="F",
        birthday=date(1998,8,27),
        registered_at=datetime.utcnow() - timedelta(hours=3),
        password_hash=generate_password_hash("user13pass")
    )
    db.session.add_all([admin, newbie])
    db.session.commit()

    # «Онлайн» 5 пользователей
    now = datetime.utcnow()
    for uid in [1,3,5,7,12]:
        u = User.query.get(uid)
        u.last_seen = now
    db.session.commit()

# === App bootstrap (важно для Render) ===
with app.app_context():
    db.create_all()
    seed_db()

# === Routes ===
@app.route("/health")
def health():
    return "ok", 200

@app.route("/", methods=["GET"])
def index():
    t0 = perf_counter()

    # визит
    db.session.add(Visit()); db.session.commit()

    now = datetime.utcnow()
    online_window = now - timedelta(minutes=5)
    online = User.query.filter(User.last_seen != None, User.last_seen > online_window).count()

    regs_total = User.query.count()
    males = User.query.filter_by(gender="M").count()
    females = User.query.filter_by(gender="F").count()
    newbies = User.query.filter(User.registered_at >= now - timedelta(hours=24)).count()

    today = date.today()
    birthdays = User.query.filter(
        User.birthday != None,
        db.extract("month", User.birthday) == today.month,
        db.extract("day", User.birthday) == today.day
    ).count()

    visits_day = Visit.query.filter(Visit.ts >= now - timedelta(hours=24)).count()

    time_str, date_str, weekday_str = now_ru()

    # первичный рендер для «Сжатия»
    html1 = render_template(
        "index.html",
        header_title="ДАВИНЧИК",
        welcome_text="Добро пожаловать",
        time_str=time_str, date_str=date_str, weekday_str=weekday_str,
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
        in_chat=online if online else 5,
        newbies=newbies, birthdays=birthdays, regs_total=regs_total,
        males=males, females=females, partners_total=7,
        visits_day=visits_day,
        perf_time="0.0000", compression_pct="63.0"
    )

    gz = gzip.compress(html1.encode("utf-8"))
    ratio = (1 - len(gz)/max(1,len(html1.encode("utf-8"))))*100
    elapsed = perf_counter() - t0

    return render_template(
        "index.html",
        header_title="ДАВИНЧИК",
        welcome_text="Добро пожаловать",
        time_str=time_str, date_str=date_str, weekday_str=weekday_str,
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
        in_chat=online if online else 5,
        newbies=newbies, birthdays=birthdays, regs_total=regs_total,
        males=males, females=females, partners_total=7,
        visits_day=visits_day,
        perf_time=f"{elapsed:.4f}", compression_pct=f"{ratio:.1f}"
    )

@app.route("/login", methods=["POST"])
def login():
    nick_or_id = request.form.get("nick","").strip()
    pwd = request.form.get("password","")
    user = None
    if nick_or_id.isdigit():
        user = User.query.get(int(nick_or_id))
    if not user:
        user = User.query.filter_by(nickname=nick_or_id).first()
    if user and check_password_hash(user.password_hash, pwd):
        user.last_seen = datetime.utcnow()
        db.session.commit()
    return redirect(url_for("index"))

# === Entry point for local run ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
