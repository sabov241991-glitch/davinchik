import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from database import Database
import json

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация базы
db = Database()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name
    
    # Создаем/получаем пользователя
    role = db.create_user(user_id, username)
    user_data = db.get_user(user_id)
    
    if user_data and not user_data[3]:  # not registered
        keyboard = [[InlineKeyboardButton("📝 Регистрация", callback_data="register")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"Добро пожаловать в *Давинчик*! 💌\n\n"
            f"Для доступа к функциям пройдите регистрацию!",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    else:
        # Показываем главное меню
        await show_main_menu(update, user_data)

async def show_main_menu(update: Update, user_data):
    user_id = user_data[0]
    role = user_data[2]
    messages_count = user_data[5]
    
    # Определяем звезды
    stars = ""
    for threshold, star in sorted(STAR_LEVELS.items(), reverse=True):
        if messages_count >= threshold:
            stars = star
            break
    
    keyboard = [
        [InlineKeyboardButton("👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton("🎮 Игры", callback_data="games")],
        [InlineKeyboardButton("📊 Рейтинг", callback_data="rating")]
    ]
    
    if role >= 2:  # Админ
        keyboard.append([InlineKeyboardButton("⚙️ Админ-панель", callback_data="admin")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"{stars} *Главное меню* {stars}\n\n"
        f"Сообщений: {messages_count}\n"
        f"Нарушений: {user_data[6]}",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

def main():
    from config import BOT_TOKEN
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    # Запуск
    application.run_polling()

if __name__ == "__main__":
    main()
