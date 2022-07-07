import numpy as np
from email import message
import telebot
import mysql.connector
from connect import host, user, password, database
from telebot import types
import connect  # подключение файла коннект для подключения к БД
import re
import time

from menus import back_to_main, one_step_back, main_menu, menu_day_of_week, menu_parity_of_week, choice_another_teacher, starosta_btn, student_btn  # подключение файла с функциями возврата в главное меню и предыдущее
from functions import choice_build, choice_website, choice_osn_podrazdeleniya, choice_tRas_tExm, about_help, choice_day_of_week, choice_parity_of_week, teacher_name_search
from sorry_message import sorry_message  # подключение файла с сообщением о неправильном вводе

mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database)

class User:
    def __init__(self, iduser):
        self. iduser = iduser
        self.idchat = ' '
        self.password = ' '
        self.group = ' '
        self.teacher_fio = ' '
        self.teacher_parity = ' '
        self.teacher_day = ' '
        self.str_notes_date = ' '
        self.btn_choice = ' '
        self.btn_choice_starosta_or_stud = ' '

mycursor = mydb.cursor()

BOT_TOKEN = "5525229543:AAF5zhi0s34PWgg0x3ufwdEAnxrrgCCLpjY"
             # "5525229543:AAF5zhi0s34PWgg0x3ufwdEAnxrrgCCLpjY"  # мой токен
             # "5581837086:AAFqDJgaaDop64v4cHA7HehlL08RNh-dTFU"  # токен Грига

bot = telebot.TeleBot(BOT_TOKEN)      # подключение к telegram-боту

@bot.message_handler(commands=['start'])     # вызов стартового меню по команде /start
def start(message):
    bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())

@bot.message_handler(commands=['about'])     # вызов стартового меню по команде /about
def about(message):
    bot.send_message(message.from_user.id, about_help())

#--------------------------------------------------------- ГЛАВНАЯ ФУНКЦИЯ С КНОПКАМИ ------------------------------------------------------
@bot.message_handler(content_types=['text'])    
def event(message): 
    if message.text == '💼 Мероприятия':  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        bot.send_message(message.from_user.id, "💼 Мероприятия", reply_markup = main_menu(message))
        User.btn_choice = message.text
        bot.register_next_step_handler(message, block_choice)
        
    elif message.text == '🏢 Консультации':  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        bot.send_message(message.from_user.id, "🏢 Консультации", reply_markup = main_menu(message))
        User.btn_choice = message.text
        bot.register_next_step_handler(message, block_choice)

    elif message.text == '📝 Заметки':
        bot.send_message(message.from_user.id,"📝 Заметки!", reply_markup = main_menu(message))
        User.btn_choice = message.text
        bot.register_next_step_handler(message, block_choice)

    elif message.text == '🎓 Основные подразделения':
        bot.send_message(message.from_user.id,"🎓 Основные подразделения", reply_markup = main_menu(message))
        bot.register_next_step_handler(message, osn_podrazdeleniya)        

    elif message.text == '📂 Полезные ссылки':
        bot.send_message(message.from_user.id,"📂 Полезные ссылки", reply_markup = main_menu(message))
        bot.register_next_step_handler(message, website)

    elif  message.text == '🏛️ Корпуса':                               
        bot.send_message(message.from_user.id,"🏛️ Корпуса", reply_markup = main_menu(message))
        bot.register_next_step_handler(message, build)

    elif message.text == '📅 Расписание':                          
        bot.send_message(message.from_user.id,"📅 Расписание", reply_markup = main_menu(message))
        bot.register_next_step_handler(message, table)
    
    elif message.text == '/start':
        start(message)

    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, event)

    else:
        bot.send_message(message.from_user.id, sorry_message())
        bot.register_next_step_handler(message, event)
#-------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------- РАССПИСАНИЯ ---------------------------------------------------------------------
@bot.message_handler(content_types=['text'])        
def table(message): 
    if message.text == '📋 Расписание преподавателя':     
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item2 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item2, btn_exit)
        bot.send_message(message.from_user.id,"📋 Расписание преподавателя", reply_markup = markup)
        #ДОЛЖНА БЫТЬ ФУНКЦИЯ СПИСОК ПРЕПОДАВАТЕЛЕЙ
        teacher_fulltable(message)
        bot.send_message(message.from_user.id, "Введите ФИО преподаватели из представленного списка")
        bot.register_next_step_handler(message, table_teacher_name)

    elif message.text == '🔔 Расписание звонков':         
        img = open('img/table_ring/ring.jpg', 'rb')
        bot.send_photo(message.from_user.id, img)
        bot.register_next_step_handler(message, table)

    elif message.text == '🗓️ Расписание занятий' or message.text == '🗒️ Расписание экзаменов':                      # РАСПИСАНИЕ ЗАНЯТИЙ или ЭКЗАМЕНОВ
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

    elif message.text == '⬆️ В главное меню' or message.text == '/start':          # выполняется переход в главное меню
        start(message)

    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, table) 

    else:
        bot.send_message(message.from_user.id, sorry_message())
        bot.register_next_step_handler(message, table)

@bot.message_handler(content_types=['text'])                # функция для вызова функции с выбором таблицы с расписанием
def choice_table(message):
    if message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)

    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, choice_table) 

    elif message.text == '⬅️ Назад':          # выполняется переход в предыдущее меню
        markup, notification  = one_step_back('📅 Расписание', message)
        bot.send_message(message.from_user.id, notification, reply_markup = markup)
        bot.register_next_step_handler(message, table)   

    else:          # выполняется переход в предыдущее меню
        way_to_table = choice_tRas_tExm (choice, message)     # вызывается функция для выбора расписания

        if way_to_table != 0:
            doc = open(f'{way_to_table.title()}', 'rb')
            bot.send_document(message.from_user.id, doc)           
            bot.register_next_step_handler(message, choice_table)

        else:
            bot.send_message(message.from_user.id, sorry_message())
            bot.register_next_step_handler(message, choice_table)   
#-------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------
@bot.message_handler(content_types=['text'])               # НАЖАТА КНОПКА "КОРПУСА"
def build(message):
    if message.text == '⬆️ В главное меню' or message.text == '/start':         # выполняется переход в главное меню
        start(message)

    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, build)   

    else:
        name, address = choice_build (message)          # вызывается функция для выбора корпуса

        if name != 0 and address != 0:
            img = open(f'img/builds/{name.title()}', 'rb')
            bot.send_photo(message.from_user.id, img)           
            bot.send_message(message.chat.id, f'{address.title()}')
            bot.register_next_step_handler(message, build)

        else:
            bot.send_message(message.from_user.id, sorry_message())
            bot.register_next_step_handler(message, build) 
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

    elif message.text == '🏖️ Вспомогательные': 
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

    elif message.text == '🏆 Спорт':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Отдел спорта ВолгГТУ")
        item2 = types.KeyboardButton("Студенческий спортивный клуб ВолгГТУ (Группа VK)")
        item3 = types.KeyboardButton("⬅️ Назад")   
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, btn_exit)
        bot.send_message(message.from_user.id,"Сайты и группы, посвященные спорту ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, useful_links) 

    elif message.text == '📚 Пароли и логины для DUMP':             # ОТСЫЛАЕТ КАРТИНКУ С ЛОГИНАМИ И ПАРОЛЯМИ ОТ DUMP.VSTU.RU
        img = open('img/table_dump_logins/parol_login_dump.jpg', 'rb')
        bot.send_photo(message.from_user.id, img)     
        bot.register_next_step_handler(message, website)

    elif message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню 
        start(message)

    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, website) 

    else:
        bot.send_message(message.from_user.id, sorry_message())
        bot.register_next_step_handler(message, website) 

@bot.message_handler(content_types=['text'])      # функция для вызова функции с выбором полезной ссылки ссылки
def useful_links(message):
    if message.text == '⬆️ В главное меню' or message.text ==  '/start' or choice == '⬆️ В главное меню':          # выполняется переход в главное меню
        start(message)
        
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, useful_links)  

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
            bot.send_message(message.from_user.id, sorry_message())
            bot.register_next_step_handler(message, useful_links)   
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

    elif message.text == '📕 Библиотека':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Расписание (Библиотека)")
        item2 = types.KeyboardButton("Группа VK (Библиотека)")
        item3 = types.KeyboardButton("Сайт (Библиотека)")
        item4 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о библиотеке ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, info_about_podrazdelenie)   

    elif message.text == '💸 Профком':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Кабинет и расписание (Профком)")
        item2 = types.KeyboardButton("Группа VK (Профком)")
        item3 = types.KeyboardButton("Сайт (Профком)")
        item4 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о профкоме ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, info_about_podrazdelenie)

    elif message.text == '🗿 2 Отдел':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Кабинет и информация (2 отдел)")
        item2 = types.KeyboardButton("Какие документы необходимы? (2 отдел)")
        item3 = types.KeyboardButton("Уже был там (2 отдел)")
        item4 = types.KeyboardButton("⬅️ Назад")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о 2-м отделе ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, info_about_podrazdelenie)
    
    elif message.text == '💰 Стипендии':    
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

    elif message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, osn_podrazdeleniya)           

    else:
        bot.send_message(message.from_user.id, sorry_message())
        bot.register_next_step_handler(message, osn_podrazdeleniya)         

@bot.message_handler(content_types=['text'])      # функция для вызова функции с выбором информации о основных подразделениях
def info_about_podrazdelenie(message):
    if message.text == '⬆️ В главное меню'  or message.text ==  '/start' or choice == '⬆️ В главное меню':          # выполняется переход в главное меню
        start(message)
        
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, info_about_podrazdelenie)    

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
            bot.send_message(message.from_user.id, sorry_message())
            bot.register_next_step_handler(message, info_about_podrazdelenie)   
#--------------------------------------------------------------------------------------------------------------------------------

#################################################### РЕГИСТРАЦИЯ #################################################################
@bot.message_handler(content_types=['text'])
def block_choice(message):                               
    if message.text == 'Войти в аккаунт':
        bot.send_message(message.from_user.id, "Чтобы войти в аккаунт введите пароль:")
        bot.register_next_step_handler(message, block_enter)

    elif message.text == 'Зарегистрироваться':
        bot.send_message(message.from_user.id, "Чтобы зарегистрироваться введите пароль:")
        bot.register_next_step_handler(message, block_reg_password)

    elif message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, block_choice) 

    else:
        bot.send_message(message.from_user.id, sorry_message())
        bot.register_next_step_handler(message, block_choice)    


@bot.message_handler(content_types=['text'])
def block_reg_password(message):                           # РЕГИСТРАЦИЯ ПАРОЛЯ

    if message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, block_reg_password) 

    elif message.text == "Зарегистрироваться" or message.text == "Войти в аккаунт":
        block_choice(message) 

    else:
        User.password = message.text
        bot.send_message(message.from_user.id, "Введите группу к которой принадлежите. Пожалуйста введите цифру, которая находится слева от вашей группы (например, введите 1, если вы из ИВТ-160):")
        bot.register_next_step_handler(message, block_reg_group) 
        group_fulltable(message)

def group_fulltable(message):          # ВЫВОД ВСЕХ ГРУПП
    try:
        bot.send_message(message.from_user.id, "Список групп:")
        mycursor.execute('SELECT idgroups, group_name FROM _groups')
        str_all_groups = ""
        for result in mycursor.fetchall():
            str_one_group = ""
            for x in result:
                str_one_group += str(x) + "  " 

            str_all_groups += str_one_group + "\n"

        bot.send_message(message.from_user.id, str_all_groups)

    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так")


@bot.message_handler(content_types=['text'])
def block_reg_group(message):                       # РЕГИСТРАЦИЯ ГРУППЫ       |       также нужно вывести список групп как с преподавателями
    User.idusers = message.from_user.id
    User.idchat = message.chat.id
    User.group = message.text

    if message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, block_reg_group)
    
    elif message.text == "Зарегистрироваться" or message.text == "Войти в аккаунт":
        block_choice(message) 
    
    else:
        try:
            sql = "INSERT INTO _users (idusers, user_chat, user_password, status_elder, idgroups) VALUE (%s, %s, %s, default, %s)"
            val = (User.idusers, User.idchat, User.password, User.group)
            mycursor.execute(sql, val)
            mydb.commit()
            bot.send_message(message.from_user.id, "Вы успешно зарегистрированы! Нажмите \"Войти в акаунт\"")
            bot.register_next_step_handler(message, block_choice)

        except:
            bot.send_message(message.from_user.id, "Вы уже зарегистрированы! Попробуйте нажать \"Войти в акаунт\"")
            bot.register_next_step_handler(message, block_choice)


@bot.message_handler(content_types=['text'])
def block_enter(message):                      # ВХОД В АККАУНТ
    User.idusers = message.from_user.id
    User.password = message.text

    if message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, block_enter)

    elif message.text == "Зарегистрироваться" or message.text == "Войти в аккаунт":
        block_choice(message) 
    
    else:
        try:
            sql = "SELECT idusers, user_password FROM _users WHERE idusers = %s AND user_password = %s"
            val = (User.idusers, User.password)
            mycursor.execute(sql, val)
            exist = mycursor.fetchall()
            
            if len(exist) == 1 :
                bot.send_message(message.from_user.id, "Вы вошли в аккаунт")
                if User.btn_choice == '💼 Мероприятия':
                    sql = "SELECT idusers, status_elder FROM _users WHERE idusers = " + str(User.idusers) + " AND status_elder = 1"
                    mycursor.execute(sql)
                    status = mycursor.fetchall()

                    if len(status) == 1 :
                        bot.send_message(message.from_user.id,"Выберите что хотите сделать с " + User.btn_choice, reply_markup = starosta_btn(User.btn_choice))
                        bot.register_next_step_handler(message, startosta_menu)
                    else:
                        bot.send_message(message.from_user.id,"Выберите что хотите сделать с " + User.btn_choice, reply_markup = student_btn(User.btn_choice))
                        bot.register_next_step_handler(message, student_menu)

                elif User.btn_choice == '🏢 Консультации':
                    sql = "SELECT idusers, status_elder FROM _users WHERE idusers = " + str(User.idusers) + " AND status_elder = 1"
                    mycursor.execute(sql)
                    status = mycursor.fetchall()

                    if len(status) == 1 :
                        bot.send_message(message.from_user.id,"Выберите что хотите сделать с " + User.btn_choice, reply_markup = starosta_btn(User.btn_choice))
                        bot.register_next_step_handler(message, startosta_menu)
                    else:
                        bot.send_message(message.from_user.id,"Выберите что хотите сделать с " + User.btn_choice, reply_markup = student_btn(User.btn_choice))
                        bot.register_next_step_handler(message, student_menu)

                elif User.btn_choice == '📝 Заметки':
                    notes_btn(message)

            else:
                bot.send_message(message.from_user.id, "Неверный пароль, либо вы не зарегистрированы!")
                bot.register_next_step_handler(message, block_enter)
        except:
            bot.send_message(message.from_user.id, "Неправильный пароль!")
            bot.register_next_step_handler(message, block_enter)


#################################################### старосты #######################################################################
@bot.message_handler(content_types=['text'])
def startosta_menu(message):                            
    if message.text == "Добавить " +  User.btn_choice:
        bot.register_next_step_handler(message, startosta_menu_add_date)
        bot.send_message(message.from_user.id, "Чтобы добавить " +  User.btn_choice + " нужно ввести ее по определенному шаблону (ГГГГ-ММ-ДД ЧЧ:ММ)\n"\
        "Скобки вводить не нужно! \nЗатем Нажмите \"Ввод (Enter)\" и теперь вы сможете записать все, что угодно в заметкку.")
     
    elif message.text == "Удалить " +  User.btn_choice:
        bot.register_next_step_handler(message, startosta_menu_delete)
        delete_date(message)
        student_getall(message)
        bot.send_message(message.from_user.id, "Удалить " +  User.btn_choice)
        bot.send_message(message.from_user.id, "Чтобы удалить " +  User.btn_choice+ ", нужно ввести ее номер (ID)")
     
    elif message.text == "Вывести все " + User.btn_choice:
        student_getall(message)
        bot.register_next_step_handler(message, startosta_menu)
     
    elif message.text == '⬆️ В главное меню':
        start(message)

    else:
        bot.send_message(message.from_user.id, sorry_message())
        bot.register_next_step_handler(message, startosta_menu)

@bot.message_handler(content_types=['text'])
def startosta_menu_add_date(message):
    delete_date(message)
    reg ='\d{4}-\d{2}-\d{2} \d{2}:\d{2}'
    User.str_notes_date = message.text

    if (re.fullmatch (reg, User.str_notes_date)):
        bot.register_next_step_handler(message, startosta_menu_add_content)
        bot.send_message(message.from_user.id, "Введите содержимое")

    elif message.text == 'Вывести все ' + User.btn_choice or message.text == 'Удалить ' + User.btn_choice or message.text == 'Добавить ' + User.btn_choice:
        startosta_menu(message)

    elif message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)

    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, startosta_menu_add_date)

    else:
        bot.send_message(message.from_user.id, "Дата и время введены неправильно! Пожалуйста, проверьте вводимое значение еще раз\
             и сверьте с шаблоном ➡️ (ГГГГ-ММ-ДД ЧЧ:ММ).\n Попробуйте еще раз:")
        bot.register_next_step_handler(message, startosta_menu_add_date)

@bot.message_handler(content_types=['text'])
def startosta_menu_add_content(message):
    str_notes_date = User.str_notes_date
    str_notes_content = message.text

    if message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)

    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, startosta_menu_add_content)
    
    else:
        if User.btn_choice == "💼 Мероприятия":
            try:
                sql = "INSERT INTO _events (events_date_time, events_content) VALUE (%s, %s)"
                val = (str_notes_date, str_notes_content)
                mycursor.execute(sql, val)
                mydb.commit()
                bot.send_message(message.from_user.id, "Ваше мероприятие успешно добавлено:")

                time.sleep (2)

                mycursor.execute('SELECT user_chat FROM _users')

                for result in mycursor.fetchall():
                    for x in result:
                        bot.send_message(chat_id=x, text="Добавлено новое мероприятие" + ":\n 📌 " + str_notes_date + "\n" + str_notes_content)                                                                                                      

                bot.register_next_step_handler(message, startosta_menu)

            except:
                bot.send_message(message.from_user.id, "Что-то пошло не так")
                bot.register_next_step_handler(message, startosta_menu)

        elif User.btn_choice == "🏢 Консультации":
            try:
                sql = "SELECT idgroups FROM _users WHERE idusers = " + str(User.idusers)
                mycursor.execute(sql)
                mygroup = mycursor.fetchall()
                for x in mygroup:
                    User.group = x[0]
            except:
                bot.send_message(message.from_user.id, "Что-то пошло не так")
                bot.register_next_step_handler(message, startosta_menu)

            try:
                sql = "INSERT INTO _consultations (consultations_date_time, consultations_content, idgroups) VALUE (%s, %s, %s)"
                val = (str_notes_date, str_notes_content, User.group)
                mycursor.execute(sql, val)
                mydb.commit()
                bot.send_message(message.from_user.id, "Ваша консультация успешно добавлена:")

                time.sleep (2)

                sql2 = "SELECT user_chat FROM _users WHERE idgroups = " + str(User.group)
                mycursor.execute(sql2)

                for result in mycursor.fetchall():
                    for x in result:
                        bot.send_message(chat_id=x, text="Добавлена новая консультация" + ":\n 📌 " + str_notes_date + "\n" + str_notes_content)                                                                                                      

                bot.register_next_step_handler(message, startosta_menu)

            except:
                bot.send_message(message.from_user.id, "Что-то пошло не так")
                bot.register_next_step_handler(message, startosta_menu)


@bot.message_handler(content_types=['text'])
def startosta_menu_delete(message):
    str_delete = message.text

    if message.text == 'Вывести все ' + User.btn_choice or message.text == 'Удалить ' + User.btn_choice or message.text == 'Добавить ' + User.btn_choice:
        startosta_menu(message)

    elif message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, startosta_menu_delete)

    elif User.btn_choice == "💼 Мероприятия":
        if search_id_delete(message, User.btn_choice):
            try:
                sql = "DELETE FROM _events WHERE idevents = " + str_delete
                mycursor.execute(sql)
                mydb.commit()
                bot.send_message(message.from_user.id, "Ваше мероприятие успешно удалено:")
                student_getall(message)
                bot.register_next_step_handler(message, startosta_menu_delete)

            except:
                bot.send_message(message.from_user.id, "Что-то пошло не так")
                bot.register_next_step_handler(message, startosta_menu)
        else:
            bot.send_message(message.from_user.id, "Ввести ID, значит ввести цифры сверху над мероприятием, справа от знака 📌.\n\n"\
                " ❗ Вводите только те ID, которые вам показаны. \n\n Попробуйте ввести ID мероприятия для удаления еще раз:")
            bot.register_next_step_handler(message, startosta_menu_delete)

    elif User.btn_choice == "🏢 Консультации":
        if search_id_delete(message, User.btn_choice):
            try:
                sql = "SELECT idgroups FROM _users WHERE idusers = " + str(User.idusers)
                mycursor.execute(sql)
                mygroup = mycursor.fetchall()
                for x in mygroup:
                    User.group = x[0]
            except:
                bot.send_message(message.from_user.id, "Что-то пошло не так")
                bot.register_next_step_handler(message, startosta_menu)

            try:
                sql2 = "DELETE FROM _consultations WHERE idconsultations = " + str_delete + " AND idgroups = " + str(User.group)
                mycursor.execute(sql2)
                mydb.commit()
                bot.send_message(message.from_user.id, "Ваша консультация успешно удалена:")
                student_getall(message)
                bot.register_next_step_handler(message, startosta_menu_delete)

            except:
                bot.send_message(message.from_user.id, "Что-то пошло не так")
                bot.register_next_step_handler(message, startosta_menu)

        else:
            bot.send_message(message.from_user.id, "Ввести ID, значит ввести цифры сверху над консультацией, справа от знака 📌.\n\n"\
                " ❗ Вводите только те ID, которые вам показаны. \n\n Попробуйте ввести ID консультации для удаления еще раз:")
            bot.register_next_step_handler(message, startosta_menu_delete)            

    else:
        bot.send_message(message.from_user.id, "Ввести ID, значит ввести цифры сверху над заметкой, справа от знака 📌. \n\n Попробуйте ввести ID заметки для удаления еще раз:")
        bot.register_next_step_handler(message, startosta_menu_delete)


def search_id_delete(message, btn_choice):         # проверка id на совпадение
    try:
        if btn_choice == "🏢 Консультации":
            try:
                sql1 = "SELECT idgroups FROM _users WHERE idusers = " + str(User.idusers)
                mycursor.execute(sql1)
                mygroup = mycursor.fetchall()
                for x in mygroup:
                    User.group = x[0]
            except:
                bot.send_message(message.from_user.id, "Что-то пошло не так")
                bot.register_next_step_handler(message, startosta_menu)

            sql = "SELECT idconsultations FROM _consultations where idconsultations = " + message.text + " and idgroups = " + str(User.group)

        elif btn_choice == "💼 Мероприятия":
            sql = "SELECT idevents FROM _events where idevents = "+"\""+message.text+"\""
            
        elif btn_choice == "📝 Заметки":
            sql = "SELECT idnotes FROM _notes where idnotes = "+"\""+message.text+"\" and idusers = " + str(User.idusers)

        mycursor.execute(sql)
        exist = mycursor.fetchall()
    
        if len(exist) == 1:
            return 1
        else:
            return 0
            
    except:
        return 0


#################################################### студентики #######################################################################
def student_getall(message):
    if User.btn_choice == "💼 Мероприятия":
        try:
                bot.send_message(message.from_user.id, "Ваши " + User.btn_choice)
                sql = "SELECT idevents, events_date_time, events_content FROM _events ORDER BY events_date_time"
                mycursor.execute(sql)
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
            bot.register_next_step_handler(message, startosta_menu)

    if User.btn_choice == "🏢 Консультации":
        try:
            sql = "SELECT idgroups FROM _users WHERE idusers = " + str(User.idusers)
            mycursor.execute(sql)
            mygroup = mycursor.fetchall()
            for x in mygroup:
                User.group = x[0]

        except:
            bot.send_message(message.from_user.id, "Что-то пошло не так")
            bot.register_next_step_handler(message, startosta_menu)

        try:
                bot.send_message(message.from_user.id, "Ваши " + User.btn_choice)
                sql = "SELECT idconsultations, consultations_date_time, consultations_content FROM _consultations WHERE idgroups = " + str(User.group) + " ORDER BY consultations_date_time"
                mycursor.execute(sql)
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
            bot.register_next_step_handler(message, startosta_menu)


@bot.message_handler(content_types=['text'])
def student_menu(message):
    if message.text == "Вывести все " + User.btn_choice:
        student_getall(message)
        bot.register_next_step_handler(message, startosta_menu)

    elif message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
        
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, notes_menu)

    else:
        bot.send_message(message.from_user.id, sorry_message())
        bot.register_next_step_handler(message, student_menu)
####################################################################################################################################

#################################################### ЗАМЕТКИ #######################################################################
def notes_btn(message):                                            
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Добавить заметку")
    item2 = types.KeyboardButton("Удалить заметку")
    item3 = types.KeyboardButton("Вывести все заметки")
    btn_exit = types.KeyboardButton("⬆️ В главное меню")
    markup.add(item1, item2, item3, btn_exit)
    bot.send_message(message.from_user.id,"Выберите что хотите сделать с заметками!", reply_markup = markup)
    bot.register_next_step_handler(message, notes_menu)


@bot.message_handler(content_types=['text'])
def notes_menu(message):                            # ДОБАВЛЕНИЕ ЗАМЕТКИ
    if message.text == 'Добавить заметку':
        bot.register_next_step_handler(message, notes_menu_add_date)
        bot.send_message(message.from_user.id, "Добавить заметку")
        bot.send_message(message.from_user.id, "Чтобы добавить заметку нужно ввести ее по определенному шаблону (ГГГГ-ММ-ДД ЧЧ:ММ)\n"\
        "Скобки вводить не нужно! \nЗатем Нажмите \"Ввод (Enter)\" и теперь вы сможете записать все, что угодно в заметкку.")

    elif message.text == 'Удалить заметку':
        bot.register_next_step_handler(message, notes_menu_delete)
        delete_date(message)

        try:
            bot.send_message(message.from_user.id, "Список ваших заметок:")
            sql = "SELECT idnotes, note_date_time, note_content FROM _notes WHERE idusers = " + str(User.idusers) + " ORDER BY note_date_time"
            mycursor.execute(sql)
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
        bot.send_message(message.from_user.id, "Чтобы удалить заметку, нужно ввести ее номер (ID)")

    elif message.text == 'Вывести все заметки':
        bot.send_message(message.from_user.id, "Вывести все заметки")
        notes_menu_getall(message)

    elif message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, notes_menu)           

    else:
        bot.send_message(message.from_user.id, sorry_message())
        bot.register_next_step_handler(message, notes_menu)    


@bot.message_handler(content_types=['text'])
def notes_menu_add_date(message):                 # ДОБАВЛЕНИЕ ДАТЫ
    delete_date(message)
    reg ='\d{4}-\d{2}-\d{2} \d{2}:\d{2}'
    User.str_notes_date = message.text

    if (re.fullmatch (reg, User.str_notes_date)):
            bot.register_next_step_handler(message, notes_menu_add_content)
            bot.send_message(message.from_user.id, "Введите содержимое")

    elif message.text == 'Вывести все заметки' or message.text == 'Удалить заметку' or message.text == 'Добавить заметку':
        notes_menu(message)

    elif message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, notes_menu_add_date)                   
      
    else:
        bot.send_message(message.from_user.id, "Дата и время введены неправильно! Пожалуйста, проверьте вводимое значение еще раз\
             и сверьте с шаблоном ➡️ (ГГГГ-ММ-ДД ЧЧ:ММ).\n Попробуйте еще раз:")    
        bot.register_next_step_handler(message, notes_menu_add_date)

@bot.message_handler(content_types=['text'])
def notes_menu_add_content(message):                  # ВВОД ДАТЫ И СОДЕРЖАНИЯ ЗАМЕТКИ
    str_notes_date = User.str_notes_date
    str_notes_content = message.text

    try:
        sql = "INSERT INTO _notes (note_date_time, note_content, idusers) VALUE (%s, %s, %s)"
        val = (str_notes_date, str_notes_content, User.idusers)
        mycursor.execute(sql, val)
        mydb.commit()
        bot.send_message(message.from_user.id, "Ваша заметка успешно добавлена:")

        bot.send_message(message.from_user.id, "Добавлена новая заметка:\n📌 " + str_notes_date + "\n" + str_notes_content)                                                                                                      

        bot.register_next_step_handler(message, notes_menu)

    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так")
        bot.register_next_step_handler(message, notes_menu)

@bot.message_handler(content_types=['text'])
def notes_menu_delete(message):               # УДАЛЕНИЕ ЗАМЕТКИ (ПО ЖЕЛАНИЮ ПОЛЬЗОВАТЕЛЯ)
    delete_date(message)
    str_delete = message.text

    if search_id_delete(message, User.btn_choice):
        try:
            sql = "DELETE FROM _notes WHERE idnotes = " + str_delete + " AND idusers = " + str(User.idusers)
            mycursor.execute(sql)
            mydb.commit()
            bot.send_message(message.from_user.id, "Ваша заметка успешно удалена:")
            notes_menu_getall(message)

        except:
            bot.send_message(message.from_user.id, "Что-то пошло не так")
            bot.register_next_step_handler(message, notes_menu)

    elif message.text == 'Вывести все заметки' or message.text == 'Удалить заметку' or message.text == 'Добавить заметку':
        notes_menu(message)

    elif message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, notes_menu_delete)

    else:
        bot.send_message(message.from_user.id, "Ввести ID, значит ввести цифры сверху над заметкой, справа от знака 📌.\n\n"\
            " ❗ Вводите только те ID, которые вам показаны. \n\n Попробуйте ввести ID заметки для удаления еще раз:")
        bot.register_next_step_handler(message, notes_menu_delete)


def notes_menu_getall(message):
    delete_date(message)                # УДАЛЕНИЕ ЗАМЕТКИ (ПО ПО ИСТЕЧЕНИИ ДАТЫ И ВРЕМЕНИ)
    try:
        bot.send_message(message.from_user.id, "Список ваших заметок:")
        sql = "SELECT idnotes, note_date_time, note_content FROM _notes WHERE idusers = " + str(User.idusers) + " ORDER BY note_date_time"
        mycursor.execute(sql)
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

def delete_date(message):
    try:
        if User.btn_choice == '💼 Мероприятия':
            mycursor.execute('DELETE FROM _events WHERE events_date_time < NOW()')
            mydb.commit()
        if User.btn_choice == '🏢 Консультации':
            mycursor.execute('DELETE FROM _consultations WHERE consultations_date_time < NOW()')
            mydb.commit()
        if User.btn_choice == '📝 Заметки':
            mycursor.execute('DELETE FROM _notes WHERE note_date_time < NOW()')
            mydb.commit()

    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так")
####################################################################################################################################

#################################################### ПРЕПОДАВАТЕЛИ #################################################################
@bot.message_handler(content_types=['text'])
def table_teacher_name(message):                         # ВВОД ИМЯ ПРЕПОДАВАТЕЛЯ 
    User.teacher_fio = message.text

    if message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, table_teacher_name)

    elif message.text == '⬅️ Назад':          # выполняется переход в главное меню
        markup, notification  = one_step_back('📅 Расписание', message)
        bot.send_message(message.from_user.id, notification, reply_markup = markup)
        bot.register_next_step_handler(message, table)

    elif teacher_name_search(message):
        bot.send_message(message.from_user.id,"Выберите какая неделя вас интересует:", reply_markup = menu_parity_of_week())
        bot.register_next_step_handler(message, table_teacher_parity)

    else:
        bot.send_message(message.from_user.id, "Введите ФИО преподавателя САПР, представленного в списке выше!\n\n"\
            "Постарайтесь ввести его точно также, как оно указано в списке, а также вы можете его скопировать и вставить в поле ввода, что снизит шанс несовпадения. Попробуйте еще раз:")
        bot.register_next_step_handler(message, table_teacher_name)

@bot.message_handler(content_types=['text'])
def table_teacher_parity(message):            # ВВОД ЧЕТНОСТИ НЕДЕЛИ
    User.teacher_parity = choice_parity_of_week(message)

    if message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, table_teacher_parity)

    elif message.text == '🔄 Выбрать другого преподавателя':
        bot.send_message(message.from_user.id,"Возвращаю список преподавателей:", reply_markup = choice_another_teacher())
        #ДОЛЖНА БЫТЬ ФУНКЦИЯ СПИСОК ПРЕПОДАВАТЕЛЕЙ
        teacher_fulltable(message)
        bot.send_message(message.from_user.id, "Введите ФИО преподаватели из представленного списка")
        bot.register_next_step_handler(message, table_teacher_name)

    elif User.teacher_parity == '1' or User.teacher_parity == '2': 
        bot.send_message(message.from_user.id,"Выберите на какой день недели нужно расписание", reply_markup = menu_day_of_week())
        bot.register_next_step_handler(message, table_teacher_day)

    else:
        bot.send_message(message.from_user.id, "Пожалуйста, выберите неделю, которая вас интересует).\n\n\
            Попробуйте, выбрать \"1️⃣ Неделя\" или \"2️⃣ Неделя\" с помощью кнопок, чтобы выбрать интересующую неделю.")
        bot.register_next_step_handler(message, table_teacher_parity)

      
@bot.message_handler(content_types=['text'])
def table_teacher_day(message):                    # ВВОД ДНЯ НЕДЕЛИ ДЛЯ РАСПИСАНИЯ ПРЕПОДАВАТЕЛЯ
    
    if message.text == '⬆️ В главное меню'  or message.text == '/start':          # выполняется переход в главное меню
        start(message)
    
    elif message.text == '/about':
        about(message)
        bot.register_next_step_handler(message, table_teacher_day)
        
    elif message.text == '↩️ Выбрать другую неделю':
        bot.send_message(message.from_user.id,"Возвращаю список преподавателей:", reply_markup = menu_parity_of_week())
        bot.register_next_step_handler(message, table_teacher_parity)

    elif choice_day_of_week(message) != 0:          # выполняется переход в главное меню
        User.teacher_day = choice_day_of_week(message)
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

    else:
        bot.send_message(message.from_user.id, "Пожалуйста, выберите день недели, на который вы хотите просмотреть расписание преподавателя, с помощью кнопок!")


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