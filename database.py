import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_path='davinchik.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                role INTEGER DEFAULT 0,
                registered BOOLEAN DEFAULT FALSE,
                registration_date TEXT,
                messages_count INTEGER DEFAULT 0,
                violations_count INTEGER DEFAULT 0,
                online_time INTEGER DEFAULT 0,
                last_online TEXT,
                photos TEXT DEFAULT '[]',
                profile_data TEXT DEFAULT '{}'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def create_user(self, user_id, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Проверяем первого пользователя
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        role = 3 if count == 0 else 0  # Первый = head_admin
        
        cursor.execute('''
            INSERT OR IGNORE INTO users 
            (user_id, username, role, registered, registration_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, role, False, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        return role
