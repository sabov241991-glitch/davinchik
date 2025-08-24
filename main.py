from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import random
from datetime import datetime, timedelta
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = 'davinchik-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10), default='unknown')
    age = db.Column(db.Integer, default=0)
    city = db.Column(db.String(50), default='')
    credits = db.Column(db.Integer, default=100)
    messages_count = db.Column(db.Integer, default=0)
    reputation = db.Column(db.Integer, default=0)
    rank = db.Column(db.String(20), default='👶 Новичок')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_online = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_moderator = db.Column(db.Boolean, default=False)
    is_vip = db.Column(db.Boolean, default=False)

class PrivateMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.String(80), nullable=False)
    to_user = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

def load_messages(room='main'):
    try:
        room_file = f'data/messages_{room}.json'
        if os.path.exists(room_file):
            with open(room_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return []

def save_messages(messages, room='main'):
    try:
        room_file = f'data/messages_{room}.json'
        with open(room_file, 'w', encoding='utf-8') as f:
            json.dump(messages[-100:], f, ensure_ascii=False, indent=2)
    except:
        pass

def get_online_count():
    return User.query.filter_by(is_online=True).count()

def get_user_rank(messages_count):
    if messages_count >= 1000:
        return '👑 Легенда'
    elif messages_count >= 500:
        return '🌟 Ветеран'
    elif messages_count >= 200:
        return '💫 Активный'
    elif messages_count >= 50:
        return '🔥 Постоянный'
    else:
        return '👶 Новичок'

@app.route('/')
def index():
    stats = {
        'online': get_online_count(),
        'total_users': User.query.count(),
        'girls': User.query.filter_by(gender='female').count(),
        'boys': User.query.filter_by(gender='male').count(),
        'total_messages': db.session.query(func.sum(User.messages_count)).scalar() or 0
    }
    return render_template('index.html', stats=stats)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        gender = request.form.get('gender', 'unknown')
        age = request.form.get('age', 0, type=int)
        
        if not username or not password:
            return render_template('register.html', error='Заполните все поля')
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Этот ник уже занят')
        
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            password=hashed_password,
            gender=gender,
            age=age,
            credits=200,
            rank='👶 Новичок'
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            session['username'] = new_user.username
            return redirect(url_for('profile'))
        except:
            return render_template('register.html', error='Ошибка регистрации')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            user.is_online = True
            user.last_seen = datetime.utcnow()
            db.session.commit()
            
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True
            
            return redirect(url_for('chat', room='main'))
        else:
            return render_template('login.html', error='Неверный логин или пароль')
    
    return render_template('login.html')

@app.route('/guest_login')
def guest_login():
    guest_id = random.randint(10000, 99999)
    guest_name = f"Гость_{guest_id}"
    
    session['guest'] = True
    session['username'] = guest_name
    session['guest_id'] = guest_id
    
    return redirect(url_for('chat', room='main'))

@app.route('/chat/<room>')
def chat(room):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = None
    if not session.get('guest'):
        user = User.query.get(session['user_id'])
        if user:
            user.is_online = True
            user.last_seen = datetime.utcnow()
            db.session.commit()
    
    rooms = {
        'main': '🔥 Общий чат',
        'flirt': '💖 Флирт и знакомства',
        'love': '❤️ Любовь и отношения',
        'music': '🎵 Музыка и кино',
        'games': '🎮 Игры и развлечения',
        'general': '🌍 Общение по интересам',
        'russian': '🇷🇺 Русский чат',
        'polite': '😊 Вежливый чат'
    }
    
    messages = load_messages(room)
    online_users = User.query.filter_by(is_online=True).all()
    
    return render_template('chat.html', 
                         username=session['username'],
                         room=room,
                         room_name=rooms.get(room, 'Чат'),
                         messages=messages[-50:],
                         online_users=online_users,
                         rooms=rooms,
                         user=user)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    room = request.form.get('room', 'main')
    message_text = request.form['message'].strip()
    username = session['username']
    
    if message_text:
        messages = load_messages(room)
        
        # Проверка команд
        if message_text.startswith('/'):
            if message_text.startswith('/me '):
                action = message_text[4:]
                message_text = f"*{username} {action}*"
            elif message_text.startswith('/w '):
                parts = message_text[3:].split(' ', 1)
                if len(parts) == 2:
                    to_user, priv_msg = parts
                    # Сохраняем приватное сообщение
                    pm = PrivateMessage(
                        from_user=username,
                        to_user=to_user,
                        message=priv_msg
                    )
                    db.session.add(pm)
                    db.session.commit()
                    return jsonify({'status': 'private', 'to': to_user})
        
        new_message = {
            'username': username,
            'message': message_text,
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'room': room
        }
        
        messages.append(new_message)
        save_messages(messages, room)
        
        # Увеличиваем счетчик сообщений для зарегистрированных пользователей
        if not session.get('guest'):
            user = User.query.get(session['user_id'])
            if user:
                user.messages_count += 1
                user.credits += 1
                user.rank = get_user_rank(user.messages_count)
                db.session.commit()
    
    return jsonify({'status': 'success'})

@app.route('/get_messages/<room>')
def get_messages(room):
    messages = load_messages(room)
    return jsonify(messages[-50:])

@app.route('/get_online_users')
def get_online_users():
    online_users = User.query.filter_by(is_online=True).all()
    users_data = [{
        'username': user.username,
        'rank': user.rank,
        'is_admin': user.is_admin,
        'is_moderator': user.is_moderator,
        'is_vip': user.is_vip
    } for user in online_users]
    
    return jsonify(users_data)

@app.route('/profile')
def profile():
    if 'username' not in session or session.get('guest'):
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('logout'))
    
    # Получаем непрочитанные сообщения
    unread_pm = PrivateMessage.query.filter_by(to_user=user.username, is_read=False).count()
    
    return render_template('profile.html', user=user, unread_pm=unread_pm)

@app.route('/private_messages')
def private_messages():
    if 'username' not in session or session.get('guest'):
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    received = PrivateMessage.query.filter_by(to_user=user.username).order_by(PrivateMessage.timestamp.desc()).all()
    sent = PrivateMessage.query.filter_by(from_user=user.username).order_by(PrivateMessage.timestamp.desc()).all()
    
    # Помечаем как прочитанные
    for msg in received:
        if not msg.is_read:
            msg.is_read = True
    db.session.commit()
    
    return render_template('private_messages.html', received=received, sent=sent)

@app.route('/send_private', methods=['POST'])
def send_private():
    if 'username' not in session or session.get('guest'):
        return jsonify({'error': 'Not authorized'}), 401
    
    to_user = request.form['to_user']
    message = request.form['message']
    from_user = session['username']
    
    pm = PrivateMessage(
        from_user=from_user,
        to_user=to_user,
        message=message
    )
    
    db.session.add(pm)
    db.session.commit()
    
    return jsonify({'status': 'success'})

@app.route('/logout')
def logout():
    if not session.get('guest'):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                user.is_online = False
                db.session.commit()
    
    session.clear()
    return redirect(url_for('index'))

@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

# Команды модерации
@app.route('/moderate', methods=['POST'])
def moderate():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or not (user.is_admin or user.is_moderator):
        return jsonify({'error': 'No permission'}), 403
    
    action = request.form['action']
    target_user = request.form['target_user']
    
    # Здесь можно добавить логику модерации
    # kick, mute, ban и т.д.
    
    return jsonify({'status': 'success', 'action': action, 'target': target_user})

# Обновляем онлайн статус
@app.before_request
def update_online_status():
    if 'user_id' in session and not session.get('guest'):
        user = User.query.get(session['user_id'])
        if user:
            user.last_seen = datetime.utcnow()
            db.session.commit()

# Периодическая очистка неактивных
def cleanup_inactive_users():
    with app.app_context():
        inactive_time = datetime.utcnow() - timedelta(minutes=5)
        User.query.filter(User.last_seen < inactive_time, User.is_online == True).update({'is_online': False})
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Запускаем очистку неактивных каждые 5 минут
    import threading
    def cleanup_task():
        while True:
            cleanup_inactive_users()
            threading.Event().wait(300)
    
    cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
    cleanup_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
