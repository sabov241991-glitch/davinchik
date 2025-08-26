from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import sqlite3
from datetime import datetime, date
import os
from pathlib import Path
import bcrypt

app = Flask(__name__,
            template_folder=Path(__file__).parent / 'templates',
            static_folder=Path(__file__).parent / 'static')

app.secret_key = 'davinchik-secret-key-2025'
app.config['DATABASE'] = 'davinchik.db'
app.config['ONLINE_TIMEOUT'] = 300

SYSTEM_USERS = {
    1: {'username': 'Система', 'password': 'system_pass', 'is_admin': False},
    2: {'username': 'Бармен', 'password': 'barman_pass', 'is_admin': False},
    3: {'username': 'Администратор', 'password': 'admin_pass', 'is_admin': True},
    4: {'username': 'Модератор', 'password': 'moder_pass', 'is_admin': True},
    5: {'username': 'Техподдержка', 'password': 'support_pass', 'is_admin': True},
    6: {'username': 'Робот', 'password': 'robot_pass', 'is_admin': False},
    7: {'username': 'Новостной_Бот', 'password': 'news_pass', 'is_admin': False},
    8: {'username': 'Игровой_Бот', 'password': 'game_pass', 'is_admin': False},
    9: {'username': 'Аниматор', 'password': 'animator_pass', 'is_admin': False},
    10: {'username': 'Ведущий', 'password': 'host_pass', 'is_admin': False},
    11: {'username': 'Охранник', 'password': 'guard_pass', 'is_admin': True},
    12: {'username': 'Admin', 'password': '123456', 'is_admin': True}
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
            posts_count INTEGER DEFAULT 0,
            status TEXT DEFAULT '~Постоянный Житель~',
            is_admin BOOLEAN DEFAULT FALSE
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            user_id INTEGER PRIMARY KEY,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    for user_id, user_data in SYSTEM_USERS.items():
        existing = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
        if not existing:
            conn.execute('''
                INSERT INTO users (id, username, password, is_admin, realname, status, posts_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, 
                user_data['username'],
                hashed_password,
                user_data['is_admin'],
                user_data['username'],
                '~Системный Аккаунт~' if user_id != 12 else '~Главный Администратор~',
                20000
            ))
        else:
            conn.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
    
    conn.commit()
    conn.close()

def update_user_activity(user_id):
    if user_id:
        conn = get_db()
        try:
            conn.execute('''
                INSERT OR REPLACE INTO user_sessions (user_id, last_activity)
                VALUES (?, CURRENT_TIMESTAMP)
            ''', (user_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating user activity: {e}")
        finally:
            conn.close()

def get_chat_stats():
    conn = get_db()
    
    online_count = conn.execute('''
        SELECT COUNT(*) as count_online FROM user_sessions 
        WHERE datetime(last_activity) > datetime('now', ?)
    ''', (f'-{app.config["ONLINE_TIMEOUT"]} seconds',)).fetchone()['count_online']
    
    today = date.today()
    birthday_count = conn.execute('''
        SELECT COUNT(*) as count_birthday FROM users 
        WHERE birth_date IS NOT NULL 
        AND strftime('%m-%d', birth_date) = ?
    ''', (today.strftime('%m-%d'),)).fetchone()['count_birthday']
    
    stats = conn.execute('''
        SELECT 
            COUNT(*) as total_reg,
            SUM(CASE WHEN gender = 'M' THEN 1 ELSE 0 END) as total_men,
            SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) as total_women,
            COUNT(CASE WHEN date(created_at) = date('now') THEN 1 END) as new_users_today
        FROM users WHERE id > 12
    ''').fetchone()
    
    conn.close()
    
    total_reg = stats['total_reg'] or 0
    total_men = stats['total_men'] or 0
    total_women = stats['total_women'] or 0
    new_users = stats['new_users_today'] or 0
    
    return {
        'online': online_count,
        'new_users': new_users,
        'birthdays': birthday_count,
        'total_reg': total_reg,
        'total_men': total_men,
        'total_women': total_women,
        'daily_visitors': 53,
        'partners': 7
    }

@app.before_request
def before_request():
    if 'user_id' in session:
        update_user_activity(session['user_id'])
    g.stats = get_chat_stats()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            update_user_activity(user['id'])
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
        birth_date = request.form.get('birth_date')
        
        if password != password_confirm:
            flash('Пароли не совпадают', 'error')
        elif len(password) < 4:
            flash('Пароль слишком короткий', 'error')
        else:
            try:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                conn = get_db()
                conn.execute('''
                    INSERT INTO users (username, password, email, realname, gender, birth_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (session['reg_username'], hashed_password, email, realname, gender, birth_date))
                conn.commit()
                user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
                conn.close()
                
                session.pop('reg_username', None)
                return redirect(url_for('welcome', user_id=user_id))
            except Exception as e:
                flash(f'Ошибка при регистрации: {str(e)}', 'error')
    
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
    
    return render_template('menu.html')

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
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            update_user_activity(user['id'])
            
            if tpl == 'wml':
                return redirect(url_for('menu'))
            elif tpl == 'xml':
                return redirect(url_for('menu'))
            else:
                return redirect(url_for('lobby'))
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
