from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.emojis import EMOJIS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Гость"
    
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['user']} Регистрация", callback_data='register')],
        [InlineKeyboardButton(f"{EMOJIS['clan']} Кланы", callback_data='clans')],
        [InlineKeyboardButton(f"{EMOJIS['game']} Игры", callback_data='games')],
        [InlineKeyboardButton(f"{EMOJIS['rating']} Рейтинг", callback_data='rating')],
        [InlineKeyboardButton(f"{EMOJIS['sign']} Комната", callback_data='room')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Добро пожаловать! *{username}* в Давинчик 💌\n\n"
        f"{EMOJIS['fire']} *Место где решают сильные* {EMOJIS['fire']}\n"
        f"{EMOJIS['star']} *Играют умные* {EMOJIS['star']}\n"
        f"{EMOJIS['dice']} *Выживают хитрые* {EMOJIS['dice']}",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
