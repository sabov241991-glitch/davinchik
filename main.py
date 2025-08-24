from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Хранилище пользователей
users = []

@app.route("/")
def index():
    return render_template("index.html", users=users)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]
        for user in users:
            if user["nickname"] == nickname and user["password"] == password:
                return redirect(url_for("index"))
        return render_template("login.html", error="Неверный ник или пароль")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        birthday = request.form["birthday"]
        country = request.form["country"]
        gender = request.form["gender"]
        about = request.form["about"]

        if password != confirm:
            return render_template("register.html", error="Пароли не совпадают!")

        users.append({
            "nickname": nickname,
            "password": password,
            "birthday": birthday,
            "country": country,
            "gender": gender,
            "about": about
        })
        return redirect(url_for("index"))
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
