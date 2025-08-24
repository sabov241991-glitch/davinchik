import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.start import start

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8271459301:AAFfJCTj061MFkMgSqbXGp9Vy8JV-XxS5u0')

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    
    application.run_polling()

if __name__ == '__main__':
    main()
