from telegram import Update
from telegram.ext import ContextTypes
from utils.emojis import EMOJIS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Гость"
    
    await update.message.reply_text(
        f"Добро пожаловать! *{username}* в Давинчик 💌\n\n"
        f"{EMOJIS['fire']} *Место где решают сильные* {EMOJIS['fire']}\n"
        f"{EMOJIS['star']} *Играют умные* {EMOJIS['star']}\n"
        f"{EMOJIS['dice']} *Выживают хитрые* {EMOJIS['dice']}",
        parse_mode='Markdown'
    )
