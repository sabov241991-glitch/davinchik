from flask import Flask, render_template, redirect, url_for, request, session
import os

app = Flask(__name__)
app.secret_key = "davinchik_secret"

# Хранилище пользователей
users = []
girls = 0
boys = 0

@app.route("/")
def home():
    return render_template("index.html", users=users, girls=girls, boys=boys)

@app.route("/register", methods=["GET", "POST"])
def register():
    global girls, boys
    if request.method == "POST":
        username = request.form["username"]
        gender = request.form["gender"]

        # если это первый юзер — даём админа
        role = "gl_admin" if len(users) == 0 else "user"

        users.append({"username": username, "gender": gender, "role": role})

        if gender == "girl":
            girls += 1
        else:
            boys += 1

        session["username"] = username
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        if any(u["username"] == username for u in users):
            session["username"] = username
            return redirect(url_for("home"))
    return render_template("login.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
