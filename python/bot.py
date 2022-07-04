import numpy as np
from email import message
import telebot
import mysql.connector
from connect import host, user, password, database
from telebot import types
import connect  # подключение файла коннект для подключения к БД
import re
import time

from menus import back_to_main, one_step_back  # подключение файла с функциями возврата в главное меню и предыдущее
from functions import choice_build, choice_website, choice_osn_podrazdeleniya, choice_tRas_tExm  # подключение файла с осн. функциями

connection_db = mysql.connector.connect(user=user, password=password, host=host, database=database)  # подключение к БД

mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database
)

mycursor = mydb.cursor()

BOT_TOKEN = "5525229543:AAF5zhi0s34PWgg0x3ufwdEAnxrrgCCLpjY"
             # "5525229543:AAF5zhi0s34PWgg0x3ufwdEAnxrrgCCLpjY"  # мой токен
             # ""5581837086:AAFqDJgaaDop64v4cHA7HehlL08RNh-dTFU""  # токен Грига

bot = telebot.TeleBot(BOT_TOKEN)      # подключение к telegram-боту

class User:
    def __init__(self, iduser):
        self. iduser = iduser
        self.idchat = ' '
        self. password = ' '
        self.teacher_fio = ' '
        self.teacher_parity = ' '
        self.teacher_day = ' '
        self.str_notes_date = ' '



@bot.message_handler(commands=['start'])     # вызов стартового меню по команде /start
def start(message):
    bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())

@bot.message_handler(commands=['about'])     # вызов стартового меню по команде /start
def about(message):
    bot.send_message(message.from_user.id, "Я - информационный бот VSTU для помощи студентам ФЭВТ 1-4 курса.\n\n"\
        "<i>Я умею следущее: </i>\n\n ✅ могу выдать расписание занятий и экзаменов студентов ФЭВТ,\n\n ✅ сохранять ваши заметки и напоминать о них,\n\n"\
        " ✅ владею информацией, во сколько и в каком кабинете находится преподаватель САПР;\n\n ✅ знаю где находятся все корпуса ВолгГТУ в Волггограде;\n\n"\
        " ✅ подскажу что делать военнообязанным (или уже отслужившим) юношам;\n\n"\
        " ✅ расскажу какие виды стипендий бывают и об их условиях получения, а также о взаимосвязи баллов сессии и размеров стипендии;\n\n"\
        " ✅ могу подсказать, какие сайты или ресурсы будут полезны студенту ФЭВТ;\n\n"\
        " ✅ ведаю, информацией о деканате ФЭВТ, библиотеке и профкоме ВолгГТУ;\n\n"\
        " ✅ могу рассказать о мероприятих, которые намечаются в ВолгГТУ в ближайшее время;\n\n"\
        " ✅ знаю когда и в каком кабинете у каждой группы ФЭВТ консультации.".format(message.from_user, bot.get_me()),  parse_mode='html')

#--------------------------------------------------------- ГЛАВНАЯ ФУНКЦИЯ С КНОПКАМИ ------------------------------------------------------
@bot.message_handler(content_types=['text'])    
def event(message): 
    if message.text == '💼 Мероприятия':
        bot.send_message(message.from_user.id, "Хай")
        
    if message.text == '🏢 Консультации':
        bot.send_message(message.from_user.id, "Хай2")

    if message.text == '📝 Заметки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Войти в аккаунт")
        item2 = types.KeyboardButton("Зарегистрироваться")
        markup.add(item1, item2)
        bot.send_message(message.from_user.id,"🕒 Заметки!", reply_markup = markup)
        bot.register_next_step_handler(message, notes_choice)

    if message.text == '🎓 Основные подразделения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("📫 Деканат ФЭВТ")
        item2 = types.KeyboardButton("📕 Библиотека")
        item3 = types.KeyboardButton("💸 Профком")
        item4 = types.KeyboardButton("🗿 2 Отдел")
        item5 = types.KeyboardButton("💰 Стипендии")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, item5, btn_exit)
        bot.send_message(message.from_user.id,"🎓 Основные подразделения", reply_markup = markup)
        bot.register_next_step_handler(message, osn_podrazdeleniya)        

    if message.text == '📂 Полезные ссылки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("🎓 Сайты ВолгГТУ")
        item2 = types.KeyboardButton("🏖️ Вспомогательные")
        item3 = types.KeyboardButton("🏆 Спорт")
        item4 = types.KeyboardButton("📚 Пароли и логины для DUMP")
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
        bot.send_message(message.from_user.id,"🏛️ Корпуса", reply_markup = markup)
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("преподавателя")
        markup.add(item1)
        bot.send_message(message.from_user.id,"Расписание преподавателя", reply_markup = markup)
        #ДОЛЖНА БЫТЬ ФУНКЦИЯ СПИСОК ПРЕПОДАВАТЕЛЕЙ
        teacher_fulltable(message)
        bot.send_message(message.from_user.id, "Введите ФИО преподаватели из представленного списка")
        bot.register_next_step_handler(message, table_teacher_name)

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
        markup, notification  = one_step_back('📅 Расписание', message)
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
    
    if message.text == '🎓 Сайты ВолгГТУ':
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

    if message.text == '🏖️ Вспомогательные': 
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

    if message.text == '🏆 Спорт':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Отдел спорта ВолгГТУ")
        item2 = types.KeyboardButton("Студенческий спортивный клуб ВолгГТУ (Группа VK)")
        item3 = types.KeyboardButton("⬅️ Назад")   
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, btn_exit)
        bot.send_message(message.from_user.id,"Сайты и группы, посвященные спорту ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, useful_links) 

    if message.text == '📚 Пароли и логины для DUMP':             # ОТСЫЛАЕТ КАРТИНКУ С ЛОГИНАМИ И ПАРОЛЯМИ ОТ DUMP.VSTU.RU
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
        markup, notification  = one_step_back('📂 Полезные ссылки', message)
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

    if message.text == '📫 Деканат ФЭВТ':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Расписание и кабинет (Деканат ФЭВТ)")
        item2 = types.KeyboardButton("Группа VK (Деканат ФЭВТ)")
        item3 = types.KeyboardButton("Рейтинговая оценка системы знаний")
        item4 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о деканате ФЭВТ", reply_markup = markup)
        bot.register_next_step_handler(message, info_about_podrazdelenie)

    if message.text == '📕 Библиотека':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Расписание (Библиотека)")
        item2 = types.KeyboardButton("Группа VK (Библиотека)")
        item3 = types.KeyboardButton("Сайт (Библиотека)")
        item4 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о библиотеке ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, info_about_podrazdelenie)   

    if message.text == '💸 Профком':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Кабинет и расписание (Профком)")
        item2 = types.KeyboardButton("Группа VK (Профком)")
        item3 = types.KeyboardButton("Сайт (Профком)")
        item4 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о профкоме ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, info_about_podrazdelenie)

    if message.text == '🗿 2 Отдел':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Кабинет и информация (2 отдел)")
        item2 = types.KeyboardButton("Какие документы необходимы? (2 отдел)")
        item3 = types.KeyboardButton("Уже был там (2 отдел)")
        item4 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о 2-м отделе ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, info_about_podrazdelenie)
    
    if message.text == '💰 Стипендии':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Какие виды стипендий бывают?")
        item2 = types.KeyboardButton("Как получить академическую стипендию?")
        item3 = types.KeyboardButton("Кто имеет право на социальную стипендию?")
        item4 = types.KeyboardButton("Как получить социальную стипендию?")
        item5 = types.KeyboardButton("Как получить социальную поддержку?")          
        item6 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о стипендиях ВолгГТУ", reply_markup = markup)
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
        markup, notification  = one_step_back('🎓 Основные подразделения', message)
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









#################################################### РЕГИСТРАЦИЯ #################################################################

@bot.message_handler(content_types=['text'])
def notes_choice(message):                               # ГЛАВНОЕ МЕНЮ ЗАМЕТОК
    if message.text == 'Войти в аккаунт':
        bot.send_message(message.from_user.id, "Введите пароль")
        bot.register_next_step_handler(message, notes_pass_enter)
    if message.text == 'Зарегистрироваться':
        bot.send_message(message.from_user.id, "Чтобы зарегистрироваться введите пароль")
        bot.register_next_step_handler(message, notes_pass_reg)

@bot.message_handler(content_types=['text'])
def notes_pass_reg(message):                           # РЕГИСТРАЦИЯ
        User.idusers = message.from_user.id
        User.idchat = message.chat.id
        User.password = message.text
        try:
            sql = "INSERT INTO _users (idusers, user_chat, user_password) VALUE (%s, %s, %s)"
            val = (User.idusers, User.idchat, User.password)
            mycursor.execute(sql, val)
            mydb.commit()
            notes_btn(message)
        except:
            bot.send_message(message.from_user.id, "Вы уже зарегистрированы")
            bot.register_next_step_handler(message, notes_choice)

@bot.message_handler(content_types=['text'])
def notes_pass_enter(message):                      # ВХОД В АККАУНТ ЗАМЕТОК
        User.idusers = message.from_user.id
        User.password = message.text
        try:
            sql = "SELECT idusers, user_password FROM _users WHERE idusers = %s AND user_password = %s"
            val = (User.idusers, User.password)
            mycursor.execute(sql, val)
            exist = mycursor.fetchall()
            if len(exist) == 1 :
                bot.send_message(message.from_user.id, "Вы вошли в аккаунт")
                notes_btn(message)
            else:
                bot.send_message(message.from_user.id, "Неверный пароль, либо вы не зарегистрированы")
        except:
            bot.send_message(message.from_user.id, "Неправильный пароль")

def notes_btn(message):                                            # КНОПКИ УПРАВЛЕНИЯ ЗАМЕТКАМИ (УДАЛИТЬ, ДОБАВИТЬ, ПОКАЗАТЬ)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Добавить заметку")
    item2 = types.KeyboardButton("Удалить заметку")
    item3 = types.KeyboardButton("Вывести все заметки")
    markup.add(item1, item2, item3)
    bot.send_message(message.from_user.id,"Выберите что хотите сделать!", reply_markup = markup)
    bot.register_next_step_handler(message, notes_menu)

@bot.message_handler(content_types=['text'])
def notes_menu(message):                            # ДОБАВЛЕНИЕ ЗАМЕТКИ
    if message.text == 'Добавить заметку':
        bot.register_next_step_handler(message, notes_menu_add_date)
        bot.send_message(message.from_user.id, "Добавить заметку")
        bot.send_message(message.from_user.id, "Что добавить заметку нужно ввести ее по определенному шаблону (ММ-ДД ЧЧ:ММ) \n Скобки вводить не нужно! \nНажмите \"Ввод (Enter)\" и теперь вы сможете записать все, что угодно в заметкку.")
    elif message.text == 'Удалить заметку':
        bot.register_next_step_handler(message, notes_menu_delete)
        notes_delete_on_date(message)
        try:
            bot.send_message(message.from_user.id, "Список ваших заметок:")
            mycursor.execute('SELECT idtest, date_time, content FROM _test ORDER BY date_time')
            str_all_task = ""
            for result in mycursor.fetchall():
                str_one_task = "📌"
                for x in result:
                    str_one_task += " " + str(x) + "\n"
                str_all_task += str_one_task + "\n"
                str_all_task += "\n"
            bot.send_message(message.from_user.id, str_all_task)
        except:
            bot.send_message(message.from_user.id, "Что-то пошло не так")
            bot.register_next_step_handler(message, notes_menu)
        bot.send_message(message.from_user.id, "Удалить заметку")
        bot.send_message(message.from_user.id, "Что удалить заметку нужно ввести ее номер (ID)")
    elif message.text == 'Вывести все заметки':
        bot.send_message(message.from_user.id, "Вывести все заметки")
        notes_menu_getall(message)
    else:
        bot.send_message(message.from_user.id, "Вы ввели / выбрали не правильный запрос")
        notes_btn(message)

@bot.message_handler(content_types=['text'])
def notes_menu_add_date(message):                 # ДОБАВЛЕНИЕ ДАТЫ
    notes_delete_on_date(message)
    reg ='\d{2}-\d{2} \d{2}:\d{2}'
    User.str_notes_date = message.text
    if (re.fullmatch (reg, User.str_notes_date)):
            bot.register_next_step_handler(message, notes_menu_add_content)
            bot.send_message(message.from_user.id, "Введите содержимое")  
    else:
        bot.send_message(message.from_user.id, "Что-то пошло не так")    
        bot.register_next_step_handler(message, notes_menu)

@bot.message_handler(content_types=['text'])
def notes_menu_add_content(message):                  # ВВОД ДАТЫ И СОДЕРЖАНИЯ ЗАМЕТКИ
    str_notes_date = "2022-" + User.str_notes_date
    str_notes_content = message.text
    try:
        sql = "INSERT INTO _test (date_time, content) VALUE (%s, %s)"
        val = (str_notes_date, str_notes_content)
        mycursor.execute(sql, val)
        mydb.commit()
        bot.send_message(message.from_user.id, "Ваша заметка успешно добавлена:")
        notes_menu_getall(message)

        time.sleep (5)
        mycursor.execute('SELECT user_chat FROM _users')
        for result in mycursor.fetchall():
            for x in result:
                bot.send_message(chat_id=x, text="Добавлена новая заметка:\n📌 " + str_notes_date + "\n" + str_notes_content)                                                                                                      

        bot.register_next_step_handler(message, notes_menu)
    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так")
        bot.register_next_step_handler(message, notes_menu)

@bot.message_handler(content_types=['text'])
def notes_menu_delete(message):               # УДАЛЕНИЕ ЗАМЕТКИ (ПО ЖЕЛАНИЮ ПОЛЬЗОВАТЕЛЯ)
    notes_delete_on_date(message)
    str_delete = message.text
    try:
        sql = "DELETE FROM _test WHERE idtest = " + str_delete
        mycursor.execute(sql)
        mydb.commit()
        bot.send_message(message.from_user.id, "Ваша заметка успешно удалена:")
        notes_menu_getall(message)
    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так")


def notes_menu_getall(message):
    notes_delete_on_date(message)                # УДАЛЕНИЕ ЗАМЕТКИ (ПО ПО ИСТЕЧЕНИИ ДАТЫ И ВРЕМЕНИ)
    try:
        bot.send_message(message.from_user.id, "Список ваших заметок:")
        mycursor.execute('SELECT idtest, date_time, content FROM _test ORDER BY date_time')
        str_all_task = ""
        for result in mycursor.fetchall():
            str_one_task = "📌"
            for x in result:
                str_one_task += " " + str(x) + "\n"
            str_all_task += str_one_task + "\n"
            str_all_task += "\n"
        bot.send_message(message.from_user.id, str_all_task)
        bot.register_next_step_handler(message, notes_menu)
    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так")
        bot.register_next_step_handler(message, notes_menu)

def notes_delete_on_date(message):
    try:
        mycursor.execute('DELETE FROM _test WHERE date_time < NOW()')
        mydb.commit()
    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так")
####################################################################################################################################

#################################################### ПРЕПОДАВАТЕЛИ #################################################################
@bot.message_handler(content_types=['text'])
def table_teacher_name(message):                         # ВВОД ИМЯ ПРЕПОДАВАТЕЛЯ 
    User.teacher_fio = message.text
    bot.send_message(message.from_user.id, "Введите четность недели")
    bot.register_next_step_handler(message, table_teacher_parity)

@bot.message_handler(content_types=['text'])
def table_teacher_parity(message):            # ВВОД ЧЕТНОСТИ НЕДЕЛИ
    User.teacher_parity = message.text
    bot.send_message(message.from_user.id, "Введите на какой день недели нужно расписание")
    bot.register_next_step_handler(message, table_teacher_day)
      
@bot.message_handler(content_types=['text'])
def table_teacher_day(message):                    # ВВОД ДНЯ НЕДЕЛИ ДЛЯ РАСПИСАНИЯ ПРЕПОДАВАТЕЛЯ
    User.teacher_day = message.text
    iterator = 0
    try: 
        sql = "select `8:30 - 10:00`,`10:10 - 11:40`, `11:50 - 13:20`, `13:40 - 15:10`, `15:20 - 16:50`, `17:00 - 18:30`, `18:35 - 20:00` from _teachers as t \
                    join _tables as tb on t.idteachers = tb.idteachers \
                    where table_day = (%s) and teacher_fio = (%s) and table_parity = (%s)"
        val = (User.teacher_day, User.teacher_fio, User.teacher_parity)
        worktime_list = ["8:30 - 10:00  ","10:10 - 11:40", "11:50 - 13:20", "13:40 - 15:10", "15:20 - 16:50", "17:00 - 18:30", "18:35 - 20:00"]

        mycursor.execute(sql, val)
        str_all_lesson = ""
        for result in mycursor.fetchall():
            for x in result:
                str_all_lesson += worktime_list[iterator] + " | " + str(x) + "\n"
                iterator += 1
        bot.send_message(message.from_user.id, str_all_lesson)
        bot.register_next_step_handler(message, table_teacher_day)      
    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так")


def teacher_fulltable(message):          # ВЫВОД ВСЕХ ПРЕПОДАВАТЕЛЕЙ
    try:
        bot.send_message(message.from_user.id, "Список преподавателей:")
        mycursor.execute('SELECT teacher_fio FROM _teachers')
        str_all_teacher = ""
        for result in mycursor.fetchall():
            for x in result:
                str_all_teacher += str(x) + "\n" 
        bot.send_message(message.from_user.id, str_all_teacher)
    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так")
####################################################################################################################################




































bot.polling(none_stop=True)