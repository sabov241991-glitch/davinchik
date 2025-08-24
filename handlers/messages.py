from telegram import Update
from telegram.ext import ContextTypes
from database.database import Database
from filters.ad_filter import contains_advertisement
from utils.time_calculator import format_online_time
from config import AUTO_PROMOTION, STAR_LEVELS

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    db = Database('davinchik.db')
    user = db.get_user(user_id)
    
    if not user or not user.registered:
        return
    
    # Проверка на рекламу
    if contains_advertisement(text):
        from handlers.moderation import ban_user
        await ban_user(user_id, 24, "Система", "Реклама")
        await update.message.delete()
        await update.message.reply_text("❌ Реклама запрещена! Бан на 24 часа.")
        return
    
    # Обновление счетчика сообщений
    user.messages_count += 1
    user.save_to_db()
    
    # Проверка авто-повышения
    await check_auto_promotion(user)
    
    # Обновление онлайн времени
    update_online_time(user)

async def check_auto_promotion(user):
    db = Database('davinchik.db')
    
    for role, requirements in AUTO_PROMOTION.items():
        if (user.messages_count >= requirements['messages'] and 
            user.violations_count <= requirements['violations'] and 
            user.role < ROLES[role]):
            
            user.role = ROLES[role]
            user.save_to_db()
            # Отправка уведомления о повышении

def update_online_time(user):
    import time
    if user.last_online:
        last_online = datetime.fromisoformat(user.last_online)
        online_time = (datetime.now() - last_online).seconds
        user.online_time += online_time
    user.last_online = datetime.now().isoformat()
    user.save_to_db()
