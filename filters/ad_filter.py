import re
from config import BLACKLIST_DOMAINS

def contains_advertisement(text: str) -> bool:
    text = text.lower()
    
    # Проверка доменов
    for domain in BLACKLIST_DOMAINS:
        if domain in text:
            return True
    
    # Проверка паттернов рекламы
    patterns = [
        r'\b(купить|продам|заказать|цена|акция|скидка|бесплатно)\b',
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        r'\b(@[a-zA-Z0-9_]+)\b'  # упоминания
    ]
    
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    return False
