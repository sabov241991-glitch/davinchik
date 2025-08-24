import os, json, re
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.secret_key = "davinchik_super_secret"
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

USERS_FILE = "data/users.json"
MSGS_FILE  = "data/messages.json"
ROOM_NAME  = "Общение"

# ------- хранилища -------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {"users": {}}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_msgs():
    if not os.path.exists(MSGS_FILE):
        return {"last_id": 0, "items": []}
    with open(MSGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_msgs(data):
    with open(MSGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_system(text):
    data = load_msgs()
    data["last_id"] += 1
    item = {
        "id": data["last_id"],
        "type": "system",
        "user": "Система",
        "text": text,
        "time": datetime.now().strftime("%H:%M")
    }
    data["items"].append(item)
    save_msgs(data)
    socketio.emit("chat:new_message", item, room=ROOM_NAME)

# кто онлайн в комнате
room_members = set()

# ------- РОУТЫ -------
@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("lobby"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        users = load_users()["users"]
        u = users.get(username)
        if not u or u["password"] != password:
            return render_template("login.html", error="Неверный логин или пароль.")
        session["username"] = username
        return redirect(url_for("lobby"))
    return render_template("login.html", error=None)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        password2 = request.form.get("password2","")
        about = request.form.get("about","").strip()

        if not username or not password:
            return render_template("register.html", error="Заполни ник и пароль.")
        if password != password2:
            return render_template("register.html", error="Пароли не совпадают.")

        data = load_users()
        if username in data["users"]:
            return render_template("register.html", error="Такой ник уже занят.")

        # первый зарегистрированный получает гл.Администратора
        role = "гл.Администратор" if len(data["users"]) == 0 else "пользователь"

        data["users"][username] = {
            "password": password,
            "about": about,
            "role": role,
            "posts": 0,
            "violations": [],      # список нарушений
            "viol_count": 0,       # счётчик
            "last_seen_id": 0,     # для прыжка к новым
            "referrals": [],
            "mute_until": 0        # unix timestamp, когда размутить (0 — не в муте)
        }
        save_users(data)

        session["username"] = username
        add_system(f"<b>Добро пожаловать {username} в Давинчик 💌</b>")
        return redirect(url_for("lobby"))
    return render_template("register.html", error=None)

@app.route("/logout")
def logout():
    user = session.pop("username", None)
    if user and user in room_members:
        room_members.discard(user)
        socketio.emit("room:count", {"count": len(room_members)}, room=ROOM_NAME)
    return redirect(url_for("login"))

@app.route("/lobby")
def lobby():
    if "username" not in session:
        return redirect(url_for("login"))
    users = load_users()["users"]
    return render_template(
        "index.html",
        username=session["username"],
        registered=len(users),
        room_count=len(room_members),
        room_name=ROOM_NAME,
        role=users[session["username"]]["role"]
    )

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("chat.html", username=session["username"], room_name=ROOM_NAME)

@app.route("/profile/<nick>")
def profile(nick):
    users = load_users()["users"]
    u = users.get(nick)
    if not u:
        return "Пользователь не найден", 404
    stars = 0
    posts = u.get("posts", 0)
    if posts >= 20000: stars = 5
    elif posts >= 10000: stars = 4
    elif posts >= 5000: stars = 3
    elif posts >= 2000: stars = 2
    elif posts >= 500: stars = 1
    return render_template("profile.html", nick=nick, u=u, stars=stars)

# API для Прихожей
@app.route("/api/stats")
def api_stats():
    users = load_users()["users"]
    return jsonify({
        "registered": len(users),
        "room_count": len(room_members),
        "room_name": ROOM_NAME
    })

# ------- простая анти-реклама (автоматический мут на 24ч) -------
adv_patterns = [
    r"(?:https?://)?t\.me/[A-Za-z0-9_]+",
    r"(приглашаю|залетай|вступай)\s+в\s+(чат|канал)",
    r"идёт\s+набор",
    r"https?://"
]
adv_re = re.compile("|".join(adv_patterns), re.IGNORECASE | re.UNICODE)

def is_muted(uobj):
    if not uobj: return False
    mu = uobj.get("mute_until", 0)
    return mu and int(mu) > int(datetime.now().timestamp())

def set_mute(username, hours=24, reason="Реклама/спам"):
    data = load_users()
    u = data["users"].get(username)
    if not u: return
    until = datetime.now() + timedelta(hours=hours)
    u["mute_until"] = int(until.timestamp())
    u["viol_count"] = u.get("viol_count", 0) + 1
    u["violations"].append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "by": "Система",
        "reason": reason,
        "until": until.strftime("%Y-%m-%d %H:%M")
    })
    save_users(data)
    add_system(f"🔒 {username} получил мут до {until.strftime('%d.%m %H:%M')} (причина: {reason}).")

# ------- SOCKETS -------
@socketio.on("chat:join")
def on_join(_data):
    if "username" not in session:
        return
    username = session["username"]
    join_room(ROOM_NAME)
    room_members.add(username)
    socketio.emit("room:count", {"count": len(room_members)}, room=ROOM_NAME)

    # история + с какого сообщения новые
    msgs = load_msgs()
    users = load_users()
    last_seen = users["users"].get(username, {}).get("last_seen_id", 0)
    emit("chat:history", {
        "items": msgs["items"],
        "last_seen_id": last_seen
    })

@socketio.on("chat:leave")
def on_leave():
    if "username" not in session:
        return
    username = session["username"]
    leave_room(ROOM_NAME)
    if username in room_members:
        room_members.discard(username)
        socketio.emit("room:count", {"count": len(room_members)}, room=ROOM_NAME)

@socketio.on("chat:mark_seen")
def on_mark_seen(data):
    last_id = int(data.get("last_id", 0))
    if "username" not in session: return
    username = session["username"]
    store = load_users()
    if username in store["users"]:
        store["users"][username]["last_seen_id"] = max(
            store["users"][username].get("last_seen_id", 0), last_id
        )
        save_users(store)

@socketio.on("chat:send")
def on_send(data):
    if "username" not in session: return
    text = (data.get("text") or "").strip()
    if not text: return
    username = session["username"]

    users = load_users()
    uobj = users["users"].get(username)
    if is_muted(uobj):
        until = datetime.fromtimestamp(int(uobj["mute_until"])).strftime("%d.%m %H:%M")
        emit("chat:new_message", {
            "id": 0, "type":"system", "user":"Система",
            "text": f"🔒 Ты в муте до {until}. Сообщение не отправлено.",
            "time": datetime.now().strftime("%H:%M")
        })
        return

    # команда «поприветствовал»
    if text.lower().startswith("/hi "):
        whom = text[4:].strip()
        add_system(f"💬 {username} поприветствовал {whom}!")
        return

    # авто-мут за рекламу/приглашения
    if adv_re.search(text):
        set_mute(username, hours=24, reason="Реклама/приглашения")
        return

    # обычное сообщение
    msgs = load_msgs()
    msgs["last_id"] += 1
    item = {
        "id": msgs["last_id"],
        "type": "user",
        "user": username,
        "text": text,
        "time": datetime.now().strftime("%H:%M")
    }
    msgs["items"].append(item)
    save_msgs(msgs)

    # счётчик постов
    uobj["posts"] = uobj.get("posts", 0) + 1
    users["users"][username] = uobj
    save_users(users)

    socketio.emit("chat:new_message", item, room=ROOM_NAME)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(USERS_FILE):
        save_users({"users": {}})
    if not os.path.exists(MSGS_FILE):
        save_msgs({"last_id": 0, "items": []})
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
