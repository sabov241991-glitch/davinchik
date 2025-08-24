import sqlite3
from typing import List, Optional
from .models import User, Profile, Clan, Announcement

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            role INTEGER DEFAULT 0,
            registered INTEGER DEFAULT 0,
            registration_date TEXT,
            clan_id INTEGER,
            clan_role INTEGER DEFAULT 0,
            rating INTEGER DEFAULT 1000,
            games_played INTEGER DEFAULT 0,
            games_won INTEGER DEFAULT 0,
            room_sign TEXT DEFAULT '',
            last_activity TEXT,
            messages_count INTEGER DEFAULT 0,
            violations_count INTEGER DEFAULT 0,
            online_time INTEGER DEFAULT 0,
            last_online TEXT,
            referral_code TEXT,
            referred_by INTEGER,
            referrals_count INTEGER DEFAULT 0
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            bio TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id: int) -> Optional[User]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return User(*user_data)
        return None
    
    def save_user(self, user: User):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user.user_id, user.username, user.role, int(user.registered),
            user.registration_date, user.clan_id, user.clan_role,
            user.rating, user.games_played, user.games_won,
            user.room_sign, user.last_activity, user.messages_count,
            user.violations_count, user.online_time, user.last_online,
            user.referral_code, user.referred_by, user.referrals_count
        ))
        conn.commit()
        conn.close()
