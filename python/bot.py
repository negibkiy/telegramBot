import telebot
import mysql.connector
from connect import host, user, password, database
from telebot import types

BOT_TOKEN = "5581837086:AAFqDJgaaDop64v4cHA7HehlL08RNh-dTFU"

bot = telebot.TeleBot(BOT_TOKEN)

mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database
)

mycursor = mydb.cursor()

@bot.message_handler(commands=['start'])
def start(message):
    #КЛАВИАТУРА НАЧАЛЬНОГО МЕНЮ
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🚲 Мероприятия")
    item2 = types.KeyboardButton("🏢 Консультации")
    item3 = types.KeyboardButton("🕒 Заметки")
    item4= types.KeyboardButton("🚁 Основные подразделения")
    item5 = types.KeyboardButton("📂 Полезные ссылки")
    item6 = types.KeyboardButton("🏫 Корпуса") 
    item7 = types.KeyboardButton("📅 Расписание")
    markup.add(item1, item2, item3, item4, item5, item6, item7)
    bot.send_message(message.from_user.id, "Привет", reply_markup = markup)

    #ПРИВЕТСВТИЕ
    bot.send_message(message.from_user.id, "Хай")


@bot.message_handler(content_types=['text'])
def event(message): 
    if message.text == '🚲 Мероприятия':
        bot.send_message(message.from_user.id, "Хай")
        
    if message.text == '🏢 Консультации':
        bot.send_message(message.from_user.id, "Хай2")

    if message.text == '🕒 Заметки':
        bot.send_message(message.from_user.id, "Хай")

    if message.text == '🚁 Основные подразделения':
        bot.send_message(message.from_user.id, "Хай")

    if message.text == '📂 Полезные ссылки':
        bot.send_message(message.from_user.id, "Хай")

    if  message.text == '🏫 Корпуса':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("А учебный корпус")
        item2 = types.KeyboardButton("Б учебный корпус")
        item3 = types.KeyboardButton("Высотный учебный корпус")
        item4 = types.KeyboardButton("Главный учебный корпус")
        item5 = types.KeyboardButton("Кировский учебный корпус")
        item6 = types.KeyboardButton("Красноармейский учебный корпус")
        item7 = types.KeyboardButton("Тракторный учебный корпус")
        markup.add(item1, item2, item3, item4, item5, item6, item7)
        bot.send_message(message.from_user.id,"📅 Расписание", reply_markup = markup)
        bot.register_next_step_handler(message, table)

    if message.text == '📅 Расписание':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Расписание преподавателя")
        item2 = types.KeyboardButton("Расписание экзаменов")
        item3 = types.KeyboardButton("Обычное расписание")
        item4 = types.KeyboardButton("Расписание звонков")
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.from_user.id,"📅 Расписание", reply_markup = markup)
        bot.register_next_step_handler(message, table)


def table(message): 
    if message.text == 'Расписание преподавателя':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("преподавателя")
        markup.add(item1)
        bot.send_message(message.from_user.id,"asd", reply_markup = markup)

def build(message):
    if  message.text == '🏫 Корпуса':
        mycursor.execute(" SELECT * FROM addresses WHERE idaddresses = '3' ")
        base = mycursor.fetchall()
        for row in base:
            text = row[1]
            photo = row[2]   #тут можно указать какое поле выбрать из бд
        bot.send_message(message.from_user.id, text)
        bot.send_photo(message.from_user.id, open(photo, 'rb'))


bot.polling(none_stop=True)