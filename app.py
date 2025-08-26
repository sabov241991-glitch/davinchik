# Системные пользователи (ID 1-12)
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
    # ВАШ АККАУНТ - Главный Администратор
    12: {'username': 'Admin', 'password': '123456', 'is_admin': True}
}

def init_db():
    conn = get_db()
    
    # Создаем таблицу пользователей
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
            status TEXT DEFAULT '~Постоянный Житель~',
            is_admin BOOLEAN DEFAULT FALSE
        )
    ''')
    
    # Создаем системных пользователей и ВАШ аккаунт
    for user_id, user_data in SYSTEM_USERS.items():
        existing = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if not existing:
            conn.execute('''
                INSERT INTO users (id, username, password, is_admin, realname, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id, 
                user_data['username'], 
                user_data['password'],
                user_data['is_admin'],
                user_data['username'],  # realname
                '~Системный Аккаунт~' if user_id != 12 else '~Главный Администратор~'
            ))
    
    conn.commit()
    
    # Получаем реальную статистику (только обычных пользователей)
    stats = conn.execute('''
        SELECT 
            COUNT(*) as total_reg,
            SUM(CASE WHEN gender = 'M' THEN 1 ELSE 0 END) as total_men,
            SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) as total_women,
            COUNT(CASE WHEN date(created_at) = date('now') THEN 1 END) as new_users_today
        FROM users WHERE id > 12
    ''').fetchone()
    
    conn.close()
    return stats
