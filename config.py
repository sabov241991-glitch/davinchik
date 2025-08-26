import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'davinchik-secret-key-2025'
    DATABASE = 'davinchik.db'
    DEBUG = True
