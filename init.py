import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, BotCommand, KeyboardButton, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, JobQueue, CallbackContext, ConversationHandler
import logging, asyncio



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
async def handle_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Ты даун?")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = update.effective_chat.id
        text_start = "Я пока нихуя не умею"

        keyboard = [
            [KeyboardButton("Нихуя")],
            [KeyboardButton("не ")],
            [KeyboardButton("умею")],
        ]
        reply_markup_keyboard = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
        await update.message.reply_text(text_start, reply_markup=reply_markup_keyboard)

def main():
    # Загружаем переменные окружения 
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")

    # Создаем Application и передаем ему токен бота.
    application = Application.builder().token(TOKEN).build()
    # Обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_keyboard))
    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    application.run_polling()




if __name__ == '__main__':
    main()
