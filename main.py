import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Добро пожаловать! {user.first_name} в Давинчик 💌\n\n"
        "🔥 Место где решают сильные 🔥\n"
        "⭐ Играют умные ⭐\n"
        "🎲 Выживают хитрые 🎲\n\n"
        "Напиши /help для списка команд"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Доступные команды:\n"
        "/start - Начать работу\n"
        "/profile - Мой профиль\n"
        "/game - Игры\n"
        "/top - Рейтинг"
    )

def main():
    application = Application.builder().token("8271459301:AAFfJCTj061MFkMgSqbXGp9Vy8JV-XxS5u0").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    application.run_polling()

if __name__ == "__main__":
    main()
