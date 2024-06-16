# Импортирование
import logging
import sqlite3
from datetime import datetime

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
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
                  ['/duration', '/date'],
                  ['/addfilm'],
                  ['/search all', '/genre all'],
                  ['/close']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
logger = logging.getLogger(__name__)

keyboard = [[InlineKeyboardButton("Посетить наш сайт 💻", url='http://127.0.0.1:5000')]]

film = []
genre = []
duration = []
description = []
date = []
time = []


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
    reply_markup = InlineKeyboardMarkup(keyboard)
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
                                    "\n", reply_markup=reply_markup)


# Поиск по фильму
async def search_film(update, context):
    count_all = 0
    count_exactly = 0
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
        await update.message.reply_text(f"Все фильмы:")
        for i in records_all:
            count_all += 1
            s = i[0]
            await update.message.reply_text(f"{count_all}. {s}")
    else:
        for j in records:
            count_exactly += 1
            a = j[1]
            b = j[2]
            c = j[3]
            d = j[4]
            f = j[5]
            await update.message.reply_text(f"{count_exactly}. \nНазвание фильма: {a}; \nЖанр фильма: {b};"
                                            f"\nДлительность: {c} минут; \nДата добавления: {f}\n"
                                            f"\n 📖 Описание:\n"
                                            f"{d}")


# Поиск по жанру
async def genre(update, context):
    count_all = 0
    count_exactly = 0
    genres = context.args[0]
    con = sqlite3.connect('../db/webproject.sql')
    cur = con.cursor()
    first = cur.execute("SELECT genre FROM films")
    records_all = first.fetchall()
    second = cur.execute("SELECT * FROM `films` WHERE `genre` LIKE ?", ("%" + genres + "%",))
    records = second.fetchall()
    cur.close()
    if genres == 'all':
        await update.message.reply_text(f"Все жанры:")
        for i in records_all:
            count_all += 1
            s = i[0]
            await update.message.reply_text(f"{count_all}. {s}")
    else:
        for j in records:
            count_exactly += 1
            a = j[1]
            b = j[2]
            c = j[3]
            d = j[4]
            f = j[5]
            await update.message.reply_text(f"{count_exactly}. \nНазвание фильма: {a}; \nЖанр фильма: {b};"
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
    dt = datetime.now().strftime('%Y-%m-%d %H:%M')
    con = sqlite3.connect("../db/webproject.sql")
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO films (film, genre, film_duration, description, adding_date, added_by) VALUES ('{film}', '{genre}',"
        f"'{duration}', '{description}', '{dt}', '8')")
    con.commit()
    await update.message.reply_text('✅ Фильм добавлен!')
    return ConversationHandler.END


async def timesearch_response(update, context):
    """Отправляет сообщение когда получена команда /time"""
    global time
    await update.message.reply_text('Укажите точное время (12:00)\n'
                                    'или укажите период времени через "-" (12:00-20:00)')
    return 1


# async def finaltime(update, context):
#     global time
#     count_exactly = 0
#     time = update.message.text
#     if "-" in time:
#         timespisok = time.split('-')
#         con = sqlite3.connect("../db/webproject.sql")
#         cur = con.cursor()
#         cur.execute(
#             f"SELECT * FROM films WHERE adding_date BETWEEN ('{timespisok[0]}') and ('{timespisok[1]}')")
#         record = cur.fetchall()
#         cur.close()
#         if record == '':
#             await update.message.reply_text('В базе данных нет ни одного фильма с таким заданным параметром.')
#         else:
#             for j in record:
#                 count_exactly += 1
#                 a = j[1]
#                 b = j[2]
#                 c = j[3]
#                 d = j[4]
#                 f = j[5]
#                 await update.message.reply_text(f"{count_exactly}. \nНазвание фильма: {a}; \nЖанр фильма: {b};"
#                                                 f"\nДлительность: {c} минут; \nДата добавления: {f}\n"
#                                                 f"\n 📖 Описание:\n"
#                                                 f"{d}")
#     elif "-" not in time:
#         print('Not in time')


async def datesearch_response(update, context):
    """Отправляет сообщение когда получена команда /date"""
    global date
    await update.message.reply_text('Укажите точную дату и время (01-01-2001 12:00)\n'
                                    'или укажите период времени через "_"'
                                    ' (01-01-2001 12:00_01-02-2001 12:00)')
    return 1


async def finaldate(update, context):
    """Отправляет сообщение когда получена команда /date"""
    global date
    count_exactly = 0
    date = update.message.text
    if "_" in date:
        datespisok = date.split('_')
        con = sqlite3.connect("../db/webproject.sql")
        cur = con.cursor()
        cur.execute(
            f"SELECT * FROM films WHERE adding_date BETWEEN ('{datespisok[0]}') and ('{datespisok[1]}')")
        record = cur.fetchall()
        cur.close()
        print(datespisok[0], datespisok[1])
        if record == '':
            await update.message.reply_text("Неправильно введена дата")
        else:
            for j in record:
                count_exactly += 1
                a = j[1]
                b = j[2]
                c = j[3]
                d = j[4]
                f = j[5]
                await update.message.reply_text(f"{count_exactly}. \nНазвание фильма: {a}; \nЖанр фильма: {b};"
                                                f"\nДлительность: {c} минут; \nДата добавления: {f}\n"
                                                f"\n 📖 Описание:\n"
                                                f"{d}")
        return ConversationHandler.END
    elif "_" not in date:
        con = sqlite3.connect("../db/webproject.sql")
        cur = con.cursor()
        cur.execute(
            f"SELECT * FROM films WHERE adding_date IS ('{date}')")
        record = cur.fetchall()
        cur.close()
        if record == '':
            await update.message.reply_text("Неправильно введена дата")
        else:
            for j in record:
                count_exactly += 1
                a = j[1]
                b = j[2]
                c = j[3]
                d = j[4]
                f = j[5]
                await update.message.reply_text(f"{count_exactly}. \nНазвание фильма: {a}; \nЖанр фильма: {b};"
                                                f"\nДлительность: {c} минут; \nДата добавления: {f}\n"
                                                f"\n 📖 Описание:\n"
                                                f"{d}")


async def durationsearch_response(update, context):
    """Отправляет сообщение когда получена команда /date"""
    global duration
    await update.message.reply_text('Укажите в минутах точную продолжительность фильма в минутах (120), '
                                    'либо период продолжительности фильма через "-" (60-120)')
    return 1


async def finalduration(update, context):
    """Отправляет сообщение когда получена команда /date"""
    global duration
    count_exactly = 0
    duration = update.message.text
    if "-" in duration:
        durationspisok = duration.split('-')
        con = sqlite3.connect("../db/webproject.sql")
        cur = con.cursor()
        cur.execute(
            f"SELECT * FROM films WHERE film_duration >= ('{durationspisok[0]}') and film_duration <= ('{durationspisok[1]}')")
        record = cur.fetchall()
        cur.close()
        print(durationspisok[0], durationspisok[1])
        if record == '':
            await update.message.reply_text("Неправильно введена продолжительность фильма")
        else:
            for j in record:
                count_exactly += 1
                a = j[1]
                b = j[2]
                c = j[3]
                d = j[4]
                f = j[5]
                await update.message.reply_text(f"{count_exactly}. \nНазвание фильма: {a}; \nЖанр фильма: {b};"
                                                f"\nДлительность: {c} минут; \nДата добавления: {f}\n"
                                                f"\n 📖 Описание:\n"
                                                f"{d}")
        return ConversationHandler.END
    elif "-" not in duration:
        con = sqlite3.connect("../db/webproject.sql")
        cur = con.cursor()
        cur.execute(
            f"SELECT * FROM films WHERE film_duration IS ('{duration}')")
        record = cur.fetchall()
        cur.close()
        if record == '':
            await update.message.reply_text("Неправильно введена продолжительность фильма")
        else:
            for j in record:
                count_exactly += 1
                a = j[1]
                b = j[2]
                c = j[3]
                d = j[4]
                f = j[5]
                await update.message.reply_text(f"{count_exactly}. \nНазвание фильма: {a}; \nЖанр фильма: {b};"
                                                f"\nДлительность: {c} минут; \nДата добавления: {f}\n"
                                                f"\n 📖 Описание:\n"
                                                f"{d}")


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

    conv_handlertime = ConversationHandler(
        entry_points=[CommandHandler('date', datesearch_response)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, finaldate)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    conv_handlerduration = ConversationHandler(
        entry_points=[CommandHandler('duration', durationsearch_response)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, finalduration)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.add_handler(conv_handlertime)
    application.add_handler(conv_handlerduration)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_film))
    application.add_handler(CommandHandler("genre", genre))
    application.add_handler(CommandHandler("time", timesearch_response))
    application.add_handler(CommandHandler("date", datesearch_response))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("duration", durationsearch_response))

    application.run_polling()


if __name__ == '__main__':
    main()
