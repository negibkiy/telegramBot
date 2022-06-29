from email import message
import telebot
import mysql.connector
from connect import host, user, password, database
from telebot import types

BOT_TOKEN = "5525229543:AAF5zhi0s34PWgg0x3ufwdEAnxrrgCCLpjY"
             # "5525229543:AAF5zhi0s34PWgg0x3ufwdEAnxrrgCCLpjY"  # мой токен
             # ""5581837086:AAFqDJgaaDop64v4cHA7HehlL08RNh-dTFU""  # токен Грига

bot = telebot.TeleBot(BOT_TOKEN)      # подключение к tlegram-боту

global choice 

@bot.message_handler(commands=['start'])     # вызов стартового меню по команде /start
def start(message):
    message_id = message.from_user.id
    back_to_main(message_id)

@bot.message_handler(content_types=['text'])     #  ГЛАВНАЯ ФУНКЦИЯ С КНОПКАМИ
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Сайты ВолгГТУ")
        item2 = types.KeyboardButton("Вспомогательные")
        item3 = types.KeyboardButton("Спорт")
        btn_exit = types.KeyboardButton("Назад")
        markup.add(item1, item2, item3, btn_exit)
        bot.send_message(message.from_user.id,"📂 Полезные ссылки", reply_markup = markup)
        bot.register_next_step_handler(message, build)

    if  message.text == '🏫 Корпуса':                               # ВЫБОР КОРПУСА
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("А учебный корпус")
        item2 = types.KeyboardButton("Б учебный корпус")
        item3 = types.KeyboardButton("Высотный учебный корпус")
        item4 = types.KeyboardButton("Главный учебный корпус")
        item5 = types.KeyboardButton("Кировский учебный корпус")
        item6 = types.KeyboardButton("Красноармейский учебный корпус")
        item7 = types.KeyboardButton("Тракторный учебный корпус")
        btn_exit = types.KeyboardButton("Назад")
        markup.add(item1, item2, item3, item4, item5, item6, item7, btn_exit)
        bot.send_message(message.from_user.id,"🏫 Корпуса", reply_markup = markup)
        bot.register_next_step_handler(message, build)

    if message.text == '📅 Расписание':                            # ВЫБОР РАСПИСАНИЯ 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Расписание преподавателя")
        item2 = types.KeyboardButton("Расписание экзаменов")
        item3 = types.KeyboardButton("Расписание занятий")
        item4 = types.KeyboardButton("Расписание звонков")
        btn_exit = types.KeyboardButton("Назад")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"📅 Расписание", reply_markup = markup)
        bot.register_next_step_handler(message, table)

@bot.message_handler(content_types=['text'])         # НАЖАТА КНОПКА "РАССПИСАНИЯ"
def table(message): 

    if message.text == 'Расписание преподавателя':     # РАСПИСАНИЕ ПРЕПОДАВАТЕЛЯ
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("преподавателя")
        markup.add(item1)
        bot.send_message(message.from_user.id,"'Расписание преподавателя", reply_markup = markup)
    
    if message.text == 'Расписание звонков':         # ЗВОНКИ
        img = open('img/table_ring/ring.jpg', 'rb')
        bot.send_photo(message.from_user.id, img)
        bot.register_next_step_handler(message, table)

    if message.text == 'Расписание занятий' or message.text == 'Расписание экзаменов':                      # РАСПИСАНИЕ ЗАНЯТИЙ

        global choice
        choice = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("1 Курс")
        item2 = types.KeyboardButton("2 Курс")
        item3 = types.KeyboardButton("3 Курс")
        item4 = types.KeyboardButton("4 Курс")
        btn_exit = types.KeyboardButton("Назад")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"Выберите курс", reply_markup = markup)
        bot.register_next_step_handler(message, table)

    if message.text == '1 Курс' and choice == 'Расписание занятий':
        doc = open('document/table_default/1_kurs_raspisanie_zanyatiy.xlsx', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, table)
    elif message.text == '1 Курс' and choice == 'Расписание экзаменов':
        doc = open('document/table_exm/1_kurs_raspisanie_exams.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, table)        

    if message.text == '2 Курс' and choice == 'Расписание занятий':
        doc = open('document/table_default/2_kurs_raspisanie_zanyatiy.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, table)
    elif message.text == '2 Курс' and choice == 'Расписание экзаменов':
        doc = open('document/table_exm/2_kurs_raspisanie_exams.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, table) 

    if message.text == '3 Курс' and choice == 'Расписание занятий':
        doc = open('document/table_default/3_kurs_raspisanie_zanyatiy.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, table)
    elif message.text == '3 Курс' and choice == 'Расписание экзаменов':
        doc = open('document/table_exm/3_kurs_raspisanie_exams.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, table)          

    if message.text == '4 Курс' and choice == 'Расписание занятий':
        doc = open('document/table_default/4_kurs_raspisanie_zanyatiy.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, table)
    elif message.text == '4 Курс' and choice == 'Расписание экзаменов':
        doc = open('document/table_exm/4_kurs_raspisanie_exams.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, table)                              

    if message.text == 'Назад':          # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        message_id = message.from_user.id
        back_to_main(message_id)
        

@bot.message_handler(content_types=['text'])               # НАЖАТА КНОПКА "КОРПУСА"
def build(message):
    if message.text == 'Высотный учебный корпус':
        img = open('img/builds/Visotka.png', 'rb')
        bot.send_photo(message.from_user.id, img)       
        bot.send_message(message.chat.id, 'Высотный учебный корпус. Адрес: Волгоград, проспект им. Ленина, 28а')
        bot.register_next_step_handler(message, build)

    if message.text == 'Главный учебный корпус':
        img = open('img/builds/GUK.png', 'rb')
        bot.send_photo(message.from_user.id, img)              
        bot.send_message(message.chat.id, 'Главный учебный корпус. Адрес: Волгоград, проспект им. Ленина, 28')
        bot.register_next_step_handler(message, build)

    if message.text == 'А учебный корпус':
        img = open('img/builds/A_korpus.png', 'rb')
        bot.send_photo(message.from_user.id, img)            
        bot.send_message(message.chat.id, 'А учебный корпус. Адрес: Волгоград, Советская, 31')
        bot.register_next_step_handler(message, build)

    if message.text == 'Б учебный корпус':
        img = open('img/builds/B_korpus.png', 'rb')
        bot.send_photo(message.from_user.id, img)
        bot.send_message(message.chat.id, 'Б учебный корпус. Адрес: Волгоград, Советская, 29')
        bot.register_next_step_handler(message, build)

    if message.text == 'Тракторный учебный корпус':
        img = open('img/builds/Traktorniy.png', 'rb')
        bot.send_photo(message.from_user.id, img)        
        bot.send_message(message.chat.id, 'Тракторный учебный корпус. Адрес: Волгоград, Дегтярёва, 2')
        bot.register_next_step_handler(message, build)

    if message.text == 'Кировский учебный корпус':
        img = open('img/builds/Kirovskiy.png', 'rb')
        bot.send_photo(message.from_user.id, img)          
        bot.send_message(message.chat.id, 'Кировский учебный корпус. Адрес: Волгоград, Армавирская, 15')
        bot.register_next_step_handler(message, build)  

    if message.text == 'Красноармейский учебный корпус':
        img = open('img/builds/Krasnoarmeyskiy.png', 'rb')
        bot.send_photo(message.from_user.id, img)           
        bot.send_message(message.chat.id, 'Красноармейский учебный корпус. Адрес: Волгоград, проспект Столетова, 8')
        bot.register_next_step_handler(message, build)

    if message.text == 'Назад':          # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        message_id = message.from_user.id
        back_to_main(message_id)


# @bot.message_handler(content_types=['text'])
# def website(messange):
#     if message.text == "dsfads":
#        bot.register_next_step_handler(message, build)

def back_to_main(message):                                     # ФУНКЦИЯ ДЛЯ ВЫЗОВА ГЛАВНОГО МЕНЮ
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

bot.polling(none_stop=True)