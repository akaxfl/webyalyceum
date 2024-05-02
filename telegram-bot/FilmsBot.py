# Импортирование
import logging
import sqlite3
from datetime import datetime

from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler
from telegram.ext import CommandHandler, ConversationHandler, filters

# Токен
BOT_TOKEN = '6678338747:AAE8w7D_JPQ3ttCp-hz9awMCzp5rbM8O2MI'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

# Клавиатуры
reply_keyboard = [['/help', '/site'],
                  ['/time', '/date'],
                  ['/work_time', '/addfilm'],
                  ['/search all', '/genre all'],
                  ['/close']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
logger = logging.getLogger(__name__)

film = []
genre = []
duration = []
description = []


# Запуск
async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    now = datetime.now()
    hour = now.hour
    if hour < 6:
        await update.message.reply_html(
            rf"👋 Здравствуйте, {user.mention_html()}! Этот бот предназначен для поиска фильмов по нашей базе данных!"
            '\n'
            '\n'
            rf"Перед началам использования бота, советую Вам прочитать небольшую справку: /help",
            reply_markup=markup
        )
    elif hour < 12:
        await update.message.reply_html(
            rf"👋 Доброе утро, {user.mention_html()}! Это недавно разработанный бот для поиска фильмов по нашей базе данных!"
            '\n'
            '\n'
            rf"Перед началам использования бота, советую Вам прочитать небольшую справку: /help",
            reply_markup=markup
        )
    elif hour < 18:
        await update.message.reply_html(
            rf"👋 Добрый день, {user.mention_html()}! Это недавно разработанный бот для поиска фильмов по нашей базе данных!"
            '\n'
            '\n'
            rf"Перед началам использования бота, советую Вам прочитать небольшую справку: /help",
            reply_markup=markup
        )
    else:
        await update.message.reply_html(
            rf"👋 Добрый вечер, {user.mention_html()}! Это недавно разработанный бот для поиска фильмов по нашей базе данных!"
            '\n'
            '\n'
            rf"Перед началам использования бота, советую Вам прочитать небольшую справку: /help",
            reply_markup=markup
        )


# Помощь
async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("🎬 Справка по использованию бота:\n"
                                    "\n"
                                    "📒 Команды:""\n"
                                    "\n"
                                    "1. /help - вызывает окно помощи."
                                    "\n"
                                    "2. /time - показывает текущее время."
                                    "\n"
                                    "3. /date - сегодняшняя дата."
                                    "\n"
                                    "4. /site - ссылка на наш сайт."
                                    "\n"
                                    "5. /addfilm - добавление фильма и жанра."
                                    "\n"
                                    "6. /work_time - время работы.\n"
                                    "\n"
                                    "🔎 Команды для поиска:\n"
                                    "\n"
                                    "1. /search all - выводит все названия фильмов в базе данных."
                                    "\n"
                                    "2. /search 'название фильма' - выводит информацию про фильм"
                                    "\n"
                                    "3. /genre all - выводит все существующие жанры фильмов в базе данных."
                                    "\n"
                                    "4. /genre 'название жанра' - выводит фильм с информацией и с задананным жанром."
                                    "\n"
                                    "5. /stop останавливает добавление фильма."
                                    "\n")


# Поиск по фильму
async def search_film(update, context):
    films = context.args[0]
    con = sqlite3.connect('../db/webproject.sql')
    cur = con.cursor()
    first = cur.execute("SELECT film FROM films")
    records_all = first.fetchall()
    second = cur.execute("SELECT * FROM `films` WHERE `film` LIKE ?", ("%" + films + "%",))
    records = second.fetchall()
    cur.close()
    print(records)
    if films == 'all':
        for i in records_all:
            s = i[0]
            await update.message.reply_text(s)
    else:
        for j in records:
            a = j[1]
            b = j[2]
            c = j[3]
            d = j[4]
            f = j[5]
            await update.message.reply_text(f"\nНазвание фильма: {a}; \nЖанр фильма: {b};"
                                            f"\nДлительность: {c} минут; \nДата добавления: {f}\n"
                                            f"\n 📖 Описание:\n"
                                            f"{d}")


# Поиск по жанру
async def genre(update, context):
    genres = context.args[0]
    con = sqlite3.connect('../db/webproject.sql')
    cur = con.cursor()
    first = cur.execute("SELECT genre FROM films")
    records_all = first.fetchall()
    second = cur.execute("SELECT * FROM `films` WHERE `genre` LIKE ?", ("%" + genres + "%",))
    records = second.fetchall()
    cur.close()
    if genres == 'all':
        for i in records_all:
            s = i[0]
            await update.message.reply_text(s)
    else:
        for j in records:
            a = j[1]
            b = j[2]
            c = j[3]
            d = j[4]
            f = j[5]
            await update.message.reply_text(f"\nНазвание фильма: {a}; \nЖанр фильма: {b};"
                                            f"\nДлительность: {c} минут; \nДата добавления: {f}\n"
                                            f"\n 📖 Описание:\n"
                                            f"{d}")


# Добавление фильма 1. Название
async def addfilms_first_response(update, context):
    global film
    await update.message.reply_text('📄 Какое будет название у фильма?')
    return 1


# Добавление фильма 2. Жанр
async def addfilms_second_response(update, context):
    global genre
    global film
    film = update.message.text
    await update.message.reply_text('⚔️ Какой жанр?')
    return 2


# Добавление фильма 3. Длительность
async def addfilms_third_response(update, context):
    global duration
    global genre
    genre = update.message.text
    await update.message.reply_text('⏰ Длина фильма?')
    return 3


# Добавление фильма 1. Описание/оценка
async def addfilms_fourth_response(update, context):
    global duration
    global description
    duration = update.message.text
    await update.message.reply_text('📑 Оцените или напишите, пожалуйста, небольшое описание фильма.')
    return 4


# Добавляем фильм!
async def addfilms_final(update, context):
    global film, genre, duration, description
    description = update.message.text
    dt = datetime.now()
    con = sqlite3.connect("../db/webproject.sql")
    cursor = con.cursor()
    cursor.execute(
        f"INSERT INTO films (film, genre, film_duration, description, adding_date, added_by) VALUES ('{film}', '{genre}',"
        f"'{duration}', '{description}', '{dt}', '8')")
    con.commit()
    await update.message.reply_text('✅ Фильм добавлен!')
    return ConversationHandler.END


# Время
async def time_command(update, context):
    """Отправляет сообщение когда получена команда /time"""
    await update.message.reply_text(datetime.now().strftime("%H:%M:%S"))


# Дата
async def date_command(update, context):
    """Отправляет сообщение когда получена команда /date"""
    await update.message.reply_text(datetime.now().strftime("%d:%m:%Y"))


# Закрываем клавиатуру
async def close_keyboard(update, context):
    await update.message.reply_text(
        "Закрываю!",
        reply_markup=ReplyKeyboardRemove()
    )


# Сайт
async def site(update, context):
    """Отправляет сообщение когда получена команда /site"""
    await update.message.reply_text(
        "🖥️ Наш сайт, который имеет те же функции, что и телеграмм бот: http://127.0.0.1:5000")


async def work_time(update, context):
    """Отправляет сообщение когда получена команда /work_time"""
    await update.message.reply_text(
        "⌛Время работы: круглосуточно.\n"
        "(когда запущен .py)")


async def stop(update, context):
    await update.message.reply_text("Останавливаю!")
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('addfilm', addfilms_first_response)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, addfilms_second_response)],

            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, addfilms_third_response)],

            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, addfilms_fourth_response)],

            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, addfilms_final)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_film))
    application.add_handler(CommandHandler("genre", genre))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("date", date_command))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("work_time", work_time))

    application.run_polling()


if __name__ == '__main__':
    main()
