import os

BOT_TOKEN = os.getenv('BOT_TOKEN', '8271459301:AAFfJCTjO6lMFkWqSqbXGp9Vy8JV-XxS5u0')
ADMIN_IDS = [123456789]
DATABASE_PATH = 'davinchik.db'

ROLES = {
    'user': 0,
    'moder': 1,
    'admin': 2,
    'head_admin': 3
}

# Настройки авто-повышения
AUTO_PROMOTION = {
    'moder': {'messages': 1000, 'violations': 0},
    'admin': {'messages': 10000, 'violations': 0}
}

# Звездочки за сообщения
STAR_LEVELS = {
    500: '⭐',
    1000: '⭐⭐',
    5000: '⭐⭐⭐',
    10000: '⭐⭐⭐⭐',
    20000: '⭐⭐⭐⭐⭐'
}

# Фильтр рекламы
BLACKLIST_DOMAINS = ['.ru', '.com', '.net', '.org', 't.me', '@', 'instagram', 'vk.com']
