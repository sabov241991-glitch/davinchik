from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.start import start
from handlers.messages import handle_message
from handlers.profile import show_profile

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('profile', show_profile))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == '__main__':
    main()
