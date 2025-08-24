from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.emojis import EMOJIS
from utils.time_calculator import format_online_time
from config import STAR_LEVELS

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = Database('davinchik.db')
    user = db.get_user(user_id)
    profile = db.get_profile(user_id)
    
    # Расчет звездочек
    stars = ""
    for threshold, star in sorted(STAR_LEVELS.items()):
        if user.messages_count >= threshold:
            stars = star
    
    # Форматирование времени онлайн
    online_time_str = format_online_time(user.online_time)
    
    # Кнопка нарушений
    violations_btn = InlineKeyboardButton(
        f"⚠️ Нарушения ({user.violations_count})", 
        callback_data=f'violations_{user_id}'
    )
    
    text = (
        f"{stars} *ПРОФИЛЬ* {stars}\n\n"
        f"👤 *{profile.name}*\n"
        f"📊 Уровень: {get_role_emoji(user.role)}\n"
        f"💌 Сообщений: {user.messages_count}\n"
        f"📅 За сегодня: {get_today_messages(user_id)}\n"
        f"⏰ Online: {online_time_str}\n"
        f"⚠️ Нарушения: {user.violations_count}\n"
        f"👥 Рефералов: {user.referrals_count}\n\n"
        f"{EMOJIS['fire']} *Статистика игр* {EMOJIS['fire']}\n"
        f"🎮 Игр: {user.games_played}\n"
        f"🏆 Побед: {user.games_won}\n"
        f"⭐ Рейтинг: {user.rating}"
    )
    
    # Кнопки для фото
    photo_keyboard = []
    for i, photo_id in enumerate(user.photos[:3]):
        photo_keyboard.append(InlineKeyboardButton(f"📸 Фото {i+1}", callback_data=f'photo_{i}'))
    
    keyboard = [
        photo_keyboard,
        [violations_btn],
        [InlineKeyboardButton("✍️ Изменить анкету", callback_data='edit_profile')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)
