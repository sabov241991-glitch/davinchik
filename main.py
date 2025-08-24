import logging
import os
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
        f"✅ Бот работает! Добро пожаловать, {user.first_name}! 🎉\n\n"
        f"🔥 ДАВИНЧИК запущен! 🔥\n"
        f"Теперь можно добавлять функции!"
    )

def main():
    # Берем токен из переменных окружения
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '8271459301:AAFfJCTj061MFkMgSqbXGp9Vy8JV-XxS5u0')
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
