import telebot
import mysql.connector
from connect import host, user, password, database
from telebot import types
BOT_TOKEN = "5525229543:AAF5zhi0s34PWgg0x3ufwdEAnxrrgCCLpjY"
             # "5525229543:AAF5zhi0s34PWgg0x3ufwdEAnxrrgCCLpjY"  # мой токен
             # ""5581837086:AAFqDJgaaDop64v4cHA7HehlL08RNh-dTFU""  # токен Грига

bot = telebot.TeleBot(BOT_TOKEN)

# mydb = mysql.connector.connect(
#   host=host,
#   user=user,
#   password=password,
#   database=database
# )

# mycursor = mydb.cursor()

@bot.message_handler(content_types=['text'])  
def main_function(message):
    if message.text == '/start' or message.text == 'Вернуться в главное меню':  # кнопки главного меню
        start (message.from_user.id)

    if message.text == '📅 Расписание':
        raspisanie(message.from_user.id)

    if  message.text == '🏫 Корпуса':
         korpusa(message.from_user.id)

    if message.text == 'Высотный учебный корпус':
        img = open('telegramBot-1/img/builds/Visotka.png', 'rb')
        bot.send_photo(message.from_user.id, img)       
        bot.send_message(message.chat.id, 'Высотный учебный корпус. Адрес: Волгоград, проспект им. Ленина, 28а')
    if message.text == 'Главный учебный корпус':
        img = open('telegramBot-1/img/builds/GUK.png', 'rb')
        bot.send_photo(message.from_user.id, img)              
        bot.send_message(message.chat.id, 'Главный учебный корпус. Адрес: Волгоград, проспект им. Ленина, 28')
    if message.text == 'А учебный корпус':
        img = open('telegramBot-1/img/builds/A_korpus.png', 'rb')
        bot.send_photo(message.from_user.id, img)            
        bot.send_message(message.chat.id, 'А учебный корпус. Адрес: Волгоград, Советская, 31')
    if message.text == 'Б учебный корпус':
        img = open('telegramBot-1/img/builds/B_korpus.png', 'rb')
        bot.send_photo(message.from_user.id, img)
        bot.send_message(message.chat.id, 'Б учебный корпус. Адрес: Волгоград, Советская, 29')
    if message.text == 'Тракторный учебный корпус':
        img = open('telegramBot-1/img/builds/Traktorniy.png', 'rb')
        bot.send_photo(message.from_user.id, img)        
        bot.send_message(message.chat.id, 'Тракторный учебный корпус. Адрес: Волгоград, Дегтярёва, 2')
    if message.text == 'Кировский учебный корпус':
        img = open('telegramBot-1/img/builds/Kirovskiy.png', 'rb')
        bot.send_photo(message.from_user.id, img)          
        bot.send_message(message.chat.id, 'Кировский учебный корпус. Адрес: Волгоград, Армавирская, 15')        
    if message.text == 'Красноармейский учебный корпус':
        img = open('telegramBot-1/img/builds/Krasnoarmeyskiy.png', 'rb')
        bot.send_photo(message.from_user.id, img)           
        bot.send_message(message.chat.id, 'Красноармейский учебный корпус. Адрес: Волгоград, проспект Столетова, 8') 

    # if message.text == '🚲 Мероприятия':
    #     bot.send_message(message.from_user.id, "Хай")
    # if message.text == '🏢 Консультации':
    #     bot.send_message(message.from_user.id, "Хай2")
    # if message.text == '🕒 Заметки':
    #     bot.send_message(message.from_user.id, "Хай")
    # if message.text == '🚁 Основные подразделения':
    #     bot.send_message(message.from_user.id, "Хай")

    # if message.text == '📂 Полезные ссылки':
    #     bot.send_message(message.from_user.id, "Хай")

    #     img = open('telegramBot-1/img/builds/B_korpus.png', 'rb')
    #     bot.send_photo(message.from_user.id, img)



def korpusa(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # кнопки корпусов
        btn1 = types.KeyboardButton('Высотный учебный корпус')
        btn2 = types.KeyboardButton('Главный учебный корпус')
        btn3 = types.KeyboardButton('А учебный корпус')
        btn4 = types.KeyboardButton('Б учебный корпус')
        btn5 = types.KeyboardButton('Тракторный учебный корпус')
        btn6 = types.KeyboardButton('Кировский учебный корпус')
        btn7 = types.KeyboardButton('Красноармейский учебный корпус')
        btn_exit = types.KeyboardButton('Вернуться в главное меню')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn_exit)
        bot.send_message(message, 'Предоставляю информацию о корпусах ВолгГТУ в Волгограде:', reply_markup=markup)

def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("🚲 Мероприятия")
        item2 = types.KeyboardButton("🏢 Консультации")
        item3 = types.KeyboardButton("🕒 Заметки")
        item4= types.KeyboardButton("🚁 Основные подразделения")
        item5 = types.KeyboardButton("📂 Полезные ссылки")
        item6 = types.KeyboardButton("🏫 Корпуса") 
        item7 = types.KeyboardButton("📅 Расписание")
        markup.add(item1, item2, item3, item4, item5, item6, item7)
        bot.send_message(message, "Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = markup)

def raspisanie(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Расписание преподавателя")
    item2 = types.KeyboardButton("Расписание экзаменов")
    item3 = types.KeyboardButton("Обычное расписание")
    item4 = types.KeyboardButton("Вернуться в главное меню")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message, "Выдаю рассписания:", reply_markup = markup)




bot.polling(none_stop=True)