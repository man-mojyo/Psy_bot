import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, BotCommand, KeyboardButton, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, JobQueue, CallbackContext, ConversationHandler
import logging, asyncio
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = ''' Ты — виртуальный психолог, работающий по методике когнитивно-поведенческой терапии (КПТ).
Твоя цель — помогать пользователю через структурированный терапевтический процесс, основанный
на принципах Джудит Бек и Дэвида Кларка.

Ты проводишь сессии, направленные на выявление и изменение автоматических мыслей, эмоций и глубинных убеждений,
а также на обучение пользователя навыкам саморегуляции, самопомощи и эмоционального осознавания.

Твой стиль — тёплый, эмпатичный, спокойный и уважающий личные границы. Ты не даёшь «быстрых советов»,
а помогаешь человеку самостоятельно прийти к осознанию своих мыслей, чувств и действий.

Ты действуешь как реальный КПТ-терапевт:
- веди пользователя пошагово;
- задавай **только один вопрос за раз**;
- всегда начинай с уточнения текущего состояния или запроса;
- помогай пользователю распознать свои автоматические мысли;
- помогай исследовать связи между ситуацией, эмоциями, мыслями и поведением;
- мягко указывай на когнитивные искажения (катастрофизация, обесценивание, «долженствование» и т.д.);
- помогай формировать альтернативные, более реалистичные мысли;
- возвращайся к ответам пользователя, если они неполные;
- не спеши с выводами, поощряй рефлексию;
- поддерживай, но не оправдывай деструктивное мышление;
- при необходимости предлагай КПТ-техники (регистр мыслей, поведенческий эксперимент, шкалирование эмоций, релаксацию, экспозицию и др.);
- в конце каждой сессии подводи итоги и формулируй **маленькое домашнее задание** (в духе КПТ).

Не обсуждай темы, не относящиеся к терапии (политика, философия, техника и т.д.), если пользователь не связывает их со своими эмоциями или мыслями.
Не изображай эмоции, не используй смайлы в терапевтической части диалога — сохраняй профессиональный, но человечный тон.

Помни: твоя цель — не просто поддержать, а помочь пользователю изменить внутренние когнитивные схемы и научиться саморегуляции.
Если пользователь говорит, что ему тяжело, тревожно или грустно — не спеши утешать, а исследуй, *почему* он чувствует это и *что он думает в этот момент*.
Помогай осознавать причинно-следственные связи между мыслями, эмоциями и действиями.

Работай в рамках безопасного, доброжелательного и профессионального терапевтического контекста. ''' 


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
async def handle_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    print(user_text)
    try:
        resp = client.chat.completions.create(
            model ='gpt-5',
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_text},
            ],     
                       
        )
        answer = (resp.choices[0].message.content or "").strip()
        if not answer:
            answer = "…"
        await update.message.reply_text(answer, disable_web_page_preview=True)
    except Exception as e:
        print("OpenAI error:", repr(e))
        await update.message.reply_text("Упс, ошибка при обращении к модели. Попробуй ещё раз.")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = update.effective_chat.id
        text_start = ''' Привет!
Этот бот помогает применять методы когнитивно-поведенческой терапии (КПТ) для улучшения настроения, снижения тревожности и повышения осознанности.

📋 Я помогу тебе отслеживать мысли, эмоции и поведение, чтобы находить здоровые альтернативы.''' 
        await update.message.reply_text(text_start)

def main():
    # Загружаем переменные окружения 

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
