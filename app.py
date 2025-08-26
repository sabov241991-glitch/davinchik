from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import os
from pathlib import Path

# Создаем экземпляр Flask с явным указанием путей
app = Flask(__name__, 
            template_folder=Path(__file__).parent / 'templates',
            static_folder=Path(__file__).parent / 'static')

app.secret_key = 'davinchik-secret-key-2025'
app.config['DATABASE'] = 'davinchik.db'

# Статистика чата
CHAT_STATS = {
    'online': 7,
    'new_users': 2,
    'birthdays': 27,
    'total_reg': 19572,
    'total_men': 11987,
    'total_women': 7585,
    'daily_visitors': 53,
    'partners': 7
}

def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            realname TEXT,
            gender TEXT DEFAULT 'M',
            birth_date TEXT,
            about TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            posts_count INTEGER DEFAULT 20000,
            status TEXT DEFAULT '~Постоянный Житель~'
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html', stats=CHAT_STATS)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                           (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('lobby'))
        else:
            flash('Неверный логин или пароль', 'error')
    
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/step1', methods=['GET', 'POST'])
def register_step1():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            conn = get_db()
            existing = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            conn.close()
            
            if existing:
                flash('Этот ник уже занят', 'error')
            else:
                session['reg_username'] = username
                return redirect(url_for('register_step2'))
    
    return render_template('register_step1.html')

@app.route('/register/step2', methods=['GET', 'POST'])
def register_step2():
    if 'reg_username' not in session:
        return redirect(url_for('register'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        email = request.form.get('email')
        realname = request.form.get('realname')
        gender = request.form.get('gender', 'M')
        
        if password != password_confirm:
            flash('Пароли не совпадают', 'error')
        elif len(password) < 4:
            flash('Пароль слишком короткий', 'error')
        else:
            try:
                conn = get_db()
                conn.execute('''
                    INSERT INTO users (username, password, email, realname, gender)
                    VALUES (?, ?, ?, ?, ?)
                ''', (session['reg_username'], password, email, realname, gender))
                conn.commit()
                user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
                conn.close()
                
                session.pop('reg_username', None)
                return redirect(url_for('welcome', user_id=user_id))
            except:
                flash('Ошибка при регистрации', 'error')
    
    return render_template('register_step2.html')

@app.route('/welcome')
def welcome():
    user_id = request.args.get('user_id')
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    if not user:
        return redirect(url_for('index'))
    
    return render_template('welcome.html', user=dict(user))

@app.route('/lobby')
def lobby():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d %B %Y")
    current_day = datetime.now().strftime("%A")
    
    return render_template('lobby.html', 
                         time=current_time,
                         date=current_date,
                         day=current_day)

@app.route('/menu')
def menu():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('menu.html', stats=CHAT_STATS)

@app.route('/exit')
def exit_chat():
    session.clear()
    return render_template('exit.html')

@app.route('/go.php')
def autologin():
    user_id = request.args.get('i')
    password = request.args.get('p')
    tpl = request.args.get('tpl', '')
    
    if user_id and password:
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE id = ? AND password = ?', 
                           (user_id, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            if tpl == 'wml':
                return redirect(url_for('menu'))
            elif tpl == 'xml':
                return redirect(url_for('menu'))
            else:
                return redirect(url_for('lobby'))
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Создаем папки если их нет
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
