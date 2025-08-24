import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "davinchik_secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///davinchik.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Инициализация БД
db.init_app(app)
with app.app_context():
    db.create_all()

# Логины
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Socket.IO: используем gevent (НЕ eventlet, НЕ werkzeug)
socketio = SocketIO(app, async_mode="gevent", cors_allowed_origins="*")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- РОУТЫ ----------
@app.route("/")
@login_required
def index():
    return render_template("index.html", user=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        flash("Неверный логин или пароль")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm", "")

        if not username or not password:
            flash("Заполни логин и пароль")
            return redirect(url_for("register"))

        if password != confirm:
            flash("Пароли не совпадают")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Такой пользователь уже существует")
            return redirect(url_for("register"))

        # Первый зарегистрированный — главный админ
        role = "gl_admin" if User.query.count() == 0 else "user"

        new_user = User(username=username, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Регистрация успешна! Войдите.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ---------- СОКЕТЫ ----------
@socketio.on("connect")
def on_connect():
    if current_user.is_authenticated:
        emit("message", {"user": "Система", "msg": f"{current_user.username} подключился."}, broadcast=True)

@socketio.on("disconnect")
def on_disconnect():
    if current_user.is_authenticated:
        emit("message", {"user": "Система", "msg": f"{current_user.username} отключился."}, broadcast=True)

@socketio.on("message")
def handle_message(text):
    username = current_user.username if current_user.is_authenticated else "Гость"
    emit("message", {"user": username, "msg": text}, broadcast=True)

# ---------- ЗАПУСК ----------
if __name__ == "__main__":
    # Flask-SocketIO сам поднимет gevent WSGI-сервер (НЕ Werkzeug)
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
