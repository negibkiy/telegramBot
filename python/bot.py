import numpy as np
from email import message
import telebot
import mysql.connector
from connect import host, user, password, database
from telebot import types
import connect  # подключение файла коннект для подключения к БД

from menus import back_to_main, one_step_back  # подключение файла с функциями возврата в главное меню и предыдущее
from functions import choice_build, choice_website, choice_osn_podrazdeleniya, choice_tRas_tExm  # подключение файла с осн. функциями

# connection_db = mysql.connector.connect(user=user, password=password, host=host, database=database)  # подключение к БД

BOT_TOKEN = "5525229543:AAF5zhi0s34PWgg0x3ufwdEAnxrrgCCLpjY"
             # "5525229543:AAF5zhi0s34PWgg0x3ufwdEAnxrrgCCLpjY"  # мой токен
             # ""5581837086:AAFqDJgaaDop64v4cHA7HehlL08RNh-dTFU""  # токен Грига

bot = telebot.TeleBot(BOT_TOKEN)      # подключение к telegram-боту

@bot.message_handler(commands=['start'])     # вызов стартового меню по команде /start
def start(message):
    bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())

@bot.message_handler(commands=['about'])     # вызов стартового меню по команде /start
def about(message):
    bot.send_message(message.from_user.id, "Я - информационный бот VSTU для помощи студентам ФЭВТ 1-4 курса.\n\n"\
        "<i>Я умею следущее: </i>\n\n ✅ выдавать расписание занятий и экзаменов,\n\n ✅ сохранять ваши заметки и напоминать о них,\n\n ✅ владею информацией,"\
        " в каком кабинете находится преподаватель САПР,\n\n ✅ знаю где находятся все корпуса ВолгГТУ в Волггограде".format(message.from_user, bot.get_me()),  parse_mode='html')

#--------------------------------------------------------- ГЛАВНАЯ ФУНКЦИЯ С КНОПКАМИ ------------------------------------------------------
@bot.message_handler(content_types=['text'])    
def event(message): 
    if message.text == '💼 Мероприятия':
        bot.send_message(message.from_user.id, "Хай")
        
    if message.text == '🏢 Консультации':
        bot.send_message(message.from_user.id, "Хай2")

    if message.text == '📝 Заметки':
        bot.send_message(message.from_user.id, "Хай")

    if message.text == '🎓 Основные подразделения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Деканат ФЭВТ")
        item2 = types.KeyboardButton("Библиотека")
        item3 = types.KeyboardButton("Профком")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, btn_exit)
        bot.send_message(message.from_user.id,"🚁 Основные подразделения", reply_markup = markup)
        bot.register_next_step_handler(message, osn_podrazdeleniya)        

    if message.text == '📂 Полезные ссылки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Сайты ВолгГТУ")
        item2 = types.KeyboardButton("Вспомогательные")
        item3 = types.KeyboardButton("Спорт")
        item4 = types.KeyboardButton("Пароли и логины для DUMP")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"📂 Полезные ссылки", reply_markup = markup)
        bot.register_next_step_handler(message, website)

    if  message.text == '🏛️ Корпуса':                               # ВЫБОР КОРПУСА
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("А учебный корпус")
        item2 = types.KeyboardButton("Б учебный корпус")
        item3 = types.KeyboardButton("Высотный учебный корпус")
        item4 = types.KeyboardButton("Главный учебный корпус")
        item5 = types.KeyboardButton("Кировский учебный корпус")
        item6 = types.KeyboardButton("Красноармейский учебный корпус")
        item7 = types.KeyboardButton("Тракторный учебный корпус")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, item7, btn_exit)
        bot.send_message(message.from_user.id,"🏫 Корпуса", reply_markup = markup)
        bot.register_next_step_handler(message, build)

    if message.text == '📅 Расписание':                            # ВЫБОР РАСПИСАНИЯ 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("📋 Расписание преподавателя")
        item2 = types.KeyboardButton("🗒️ Расписание экзаменов")
        item3 = types.KeyboardButton("🗓️ Расписание занятий")
        item4 = types.KeyboardButton("🔔 Расписание звонков")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"📅 Расписание", reply_markup = markup)
        bot.register_next_step_handler(message, table)
    
    if message.text == '/start':
        start(message)
    if message.text == '/about':
        about(message) 
#-------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------- РАССПИСАНИЯ ---------------------------------------------------------------------
@bot.message_handler(content_types=['text'])        
def table(message): 
    if message.text == '📋 Расписание преподавателя':     
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        item1 = types.KeyboardButton("преподавателя")
        markup.add(item1)
        bot.send_message(message.from_user.id,"'Расписание преподавателя", reply_markup = markup)
    
    if message.text == '🔔 Расписание звонков':         
        img = open('img/table_ring/ring.jpg', 'rb')
        bot.send_photo(message.from_user.id, img)
        bot.register_next_step_handler(message, table)

    if message.text == '🗓️ Расписание занятий' or message.text == '🗒️ Расписание экзаменов':                      # РАСПИСАНИЕ ЗАНЯТИЙ или ЭКЗАМЕНОВ
        global choice 
        choice = message.text                # глобальная переменная для выбора между "расписанием экзхаменов" или "расписанием занятий"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("1 Курс")
        item2 = types.KeyboardButton("2 Курс")
        item3 = types.KeyboardButton("3 Курс")
        item4 = types.KeyboardButton("4 Курс")
        item5 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, item5, btn_exit)
        bot.send_message(message.from_user.id,"Выберите курс", reply_markup = markup)
        bot.register_next_step_handler(message, choice_table)

    if message.text == '⬆️ В главное меню' or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    if message.text == '/about':
        about(message) 

@bot.message_handler(content_types=['text'])                # функция для вызова функции с выбором таблицы с расписанием
def choice_table(message):
    if message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    elif message.text == '/about':
        about(message) 
    elif message.text == '⬅️ Назад':          # выполняется переход в главное меню
        markup, notification  = one_step_back('Расписание', message)
        bot.send_message(message.from_user.id, notification, reply_markup = markup)
        bot.register_next_step_handler(message, table)   
    else:
        way_to_table = choice_tRas_tExm (choice, message)     # вызывается функция для выбора расписания
        if way_to_table != 0:
            doc = open(f'{way_to_table.title()}', 'rb')
            bot.send_document(message.from_user.id, doc)           
            bot.register_next_step_handler(message, choice_table)
        else:
            start(message)       
#-------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------
@bot.message_handler(content_types=['text'])               # НАЖАТА КНОПКА "КОРПУСА"
def build(message):
    if message.text == '⬆️ В главное меню' or message.text == '/start':         # выполняется переход в главное меню
        start(message)
    elif message.text == '/about':
        about(message) 
    else:
        name, address = choice_build (message)          # вызывается функция для выбора корпуса
        if name != 0 and address != 0:
            img = open(f'img/builds/{name.title()}', 'rb')
            bot.send_photo(message.from_user.id, img)           
            bot.send_message(message.chat.id, f'{address.title()}')
            bot.register_next_step_handler(message, build)
        else:
            start(message)
#-------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------- ПОЛЕЗНЫЕ ССЫЛКИ -----------------------------------------------------------------
@bot.message_handler(content_types=['text'])      
def website(message):
    global choice 
    choice = message.text  # какой полезный ресурс нужен
    
    if message.text == 'Сайты ВолгГТУ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("edu")
        item2 = types.KeyboardButton("eos2")
        item3 = types.KeyboardButton("Главная страница ВолгГТУ")
        item4 = types.KeyboardButton("Рейтинг студента")
        item5 = types.KeyboardButton("DUMP - Хранилище")
        item6 = types.KeyboardButton("Библиотека")
        item7 = types.KeyboardButton("Деканат ФЭВТ (VK группа)")
        item8 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, btn_exit)
        bot.send_message(message.from_user.id,"Основные официальные сайты и группы ФЭВТ ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, useful_links)

    if message.text == 'Вспомогательные': 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Diagrams.net")
        item2 = types.KeyboardButton("ERDPlus")
        item3 = types.KeyboardButton("Iconfinder - картинки для приложений")
        item4 = types.KeyboardButton("Online Color Picker")
        item5 = types.KeyboardButton("sistemas - картинки для приложений")
        item6 = types.KeyboardButton("Антиплагиат")
        item7 = types.KeyboardButton("Перевод двоичного кода в текст онлайн")
        item8 = types.KeyboardButton("Решение СЛАУ онлайн")
        item9 = types.KeyboardButton("Определитель матрицы онлайн") 
        item10 = types.KeyboardButton("GeoGebra")
        item11 = types.KeyboardButton("⬅️ Назад")        
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9,  item10, item11, btn_exit)
        bot.send_message(message.from_user.id,"Сайты для помощи студентам ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, useful_links)      

    if message.text == 'Спорт':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Отдел спорта ВолгГТУ")
        item2 = types.KeyboardButton("Студенческий спортивный клуб ВолгГТУ (Группа VK)")
        item3 = types.KeyboardButton("⬅️ Назад")   
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, btn_exit)
        bot.send_message(message.from_user.id,"Сайты и группы, посвященные спорту ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, useful_links) 

    if message.text == 'Пароли и логины для DUMP':             # ОТСЫЛАЕТ КАРТИНКУ С ЛОГИНАМИ И ПАРОЛЯМИ ОТ DUMP.VSTU.RU
        img = open('img/table_dump_logins/parol_login_dump.jpg', 'rb')
        bot.send_photo(message.from_user.id, img)     
        bot.register_next_step_handler(message, website)

    if message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню 
        start(message)
    if message.text == '/about':
        about(message) 

@bot.message_handler(content_types=['text'])      # функция для вызова функции с выбором полезной ссылки ссылки
def useful_links(message):
    if message.text == '⬆️ В главное меню' or message.text ==  '/start' or choice == '⬆️ В главное меню':          # выполняется переход в главное меню
        start(message)
    elif message.text == '/about':
        about(message) 
    elif message.text == '⬅️ Назад':          # выполняется переход в главное меню
        markup, notification  = one_step_back('Полезные ссылки', message)
        bot.send_message(message.from_user.id, notification, reply_markup = markup)
        bot.register_next_step_handler(message, website) 
    else:
        link = choice_website(choice, message)
        if link != 0:
            bot.send_message(message.chat.id, link)
            bot.register_next_step_handler(message, useful_links)
        else:
            start(message)
#-------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------- ОСНОВНЫЕ ПОДРАЗДЕЛЕНИЯ ----------------------------------------------------------
@bot.message_handler(content_types=['text'])      
def osn_podrazdeleniya(message):
    global choice 
    choice = message.text  # какое основное подразделение нас интересует

    if message.text == 'Деканат ФЭВТ':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Расписание и кабинет (Деканат ФЭВТ)")
        item2 = types.KeyboardButton("Группа VK (Деканат ФЭВТ)")
        item3 = types.KeyboardButton("Рейтинговая оценка системы знаний")
        item4 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о деканате ФЭВТ", reply_markup = markup)
        bot.register_next_step_handler(message, info_about_podrazdelenie)

    if message.text == 'Библиотека':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Расписание (Библиотека)")
        item2 = types.KeyboardButton("Группа VK (Библиотека)")
        item3 = types.KeyboardButton("Сайт (Библиотека)")
        item4 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о библиотеке ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, info_about_podrazdelenie)   

    if message.text == 'Профком':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Кабинет и расписание (Профком)")
        item2 = types.KeyboardButton("Группа VK (Профком)")
        item3 = types.KeyboardButton("Сайт (Профком)")
        item4 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о профкоме ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, info_about_podrazdelenie)

    if message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    if message.text == '/about':
        about(message)         

@bot.message_handler(content_types=['text'])      # функция для вызова функции с выбором информации о основных подразделениях
def info_about_podrazdelenie(message):
    if message.text == '⬆️ В главное меню'  or message.text ==  '/start' or choice == '⬆️ В главное меню':          # выполняется переход в главное меню
        start(message)
    elif message.text == '/about':
        about(message) 
    elif message.text == '⬅️ Назад':          # выполняется переход в главное меню
        markup, notification  = one_step_back('Основные подразделения', message)
        bot.send_message(message.from_user.id, notification, reply_markup = markup)
        bot.register_next_step_handler(message, osn_podrazdeleniya)
    else:
        info = choice_osn_podrazdeleniya(choice, message)
        if info != 0:
            bot.send_message(message.chat.id, info)
            bot.register_next_step_handler(message, info_about_podrazdelenie)
        else:
            start(message)            
#-------------------------------------------------------------------------------------------------------------------------------------------







bot.polling(none_stop=True)