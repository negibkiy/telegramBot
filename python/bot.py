import numpy as np
from email import message
import telebot
import mysql.connector
from connect import host, user, password, database
from telebot import types
import connect  # подключение файла коннект для подключения к БД

from back_to_main import back_to_main

# connection_db = mysql.connector.connect(user=user, password=password, host=host, database=database)  # подключение к БД

BOT_TOKEN = "5525229543:AAF5zhi0s34PWgg0x3ufwdEAnxrrgCCLpjY"
             # "5525229543:AAF5zhi0s34PWgg0x3ufwdEAnxrrgCCLpjY"  # мой токен
             # ""5581837086:AAFqDJgaaDop64v4cHA7HehlL08RNh-dTFU""  # токен Грига

bot = telebot.TeleBot(BOT_TOKEN)      # подключение к telegram-боту

@bot.message_handler(commands=['start'])     # вызов стартового меню по команде /start
def start(message):
    bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())


@bot.message_handler(content_types=['text'])     #  ГЛАВНАЯ ФУНКЦИЯ С КНОПКАМИ
def event(message): 
    if message.text == '🚲 Мероприятия':
        bot.send_message(message.from_user.id, "Хай")
        
    if message.text == '🏢 Консультации':
        bot.send_message(message.from_user.id, "Хай2")

    if message.text == '🕒 Заметки':
        bot.send_message(message.from_user.id, "Хай")

    if message.text == '🚁 Основные подразделения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Деканат ФЭВТ")
        item2 = types.KeyboardButton("Библиотека")
        item3 = types.KeyboardButton("Профком")
        btn_exit = types.KeyboardButton("В главное меню")
        markup.add(item1, item2, item3, btn_exit)
        bot.send_message(message.from_user.id,"🚁 Основные подразделения", reply_markup = markup)
        bot.register_next_step_handler(message, osn_podrazdeleniya)        

    if message.text == '📂 Полезные ссылки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Сайты ВолгГТУ")
        item2 = types.KeyboardButton("Вспомогательные")
        item3 = types.KeyboardButton("Спорт")
        item4 = types.KeyboardButton("Пароли и логины для DUMP")
        btn_exit = types.KeyboardButton("В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"📂 Полезные ссылки", reply_markup = markup)
        bot.register_next_step_handler(message, website)

    if  message.text == '🏫 Корпуса':                               # ВЫБОР КОРПУСА
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("А учебный корпус")
        item2 = types.KeyboardButton("Б учебный корпус")
        item3 = types.KeyboardButton("Высотный учебный корпус")
        item4 = types.KeyboardButton("Главный учебный корпус")
        item5 = types.KeyboardButton("Кировский учебный корпус")
        item6 = types.KeyboardButton("Красноармейский учебный корпус")
        item7 = types.KeyboardButton("Тракторный учебный корпус")
        btn_exit = types.KeyboardButton("В главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, item7, btn_exit)
        bot.send_message(message.from_user.id,"🏫 Корпуса", reply_markup = markup)
        bot.register_next_step_handler(message, build)

    if message.text == '📅 Расписание':                            # ВЫБОР РАСПИСАНИЯ 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Расписание преподавателя")
        item2 = types.KeyboardButton("Расписание экзаменов")
        item3 = types.KeyboardButton("Расписание занятий")
        item4 = types.KeyboardButton("Расписание звонков")
        btn_exit = types.KeyboardButton("В главное меню")
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

    if message.text == 'Расписание занятий' or message.text == 'Расписание экзаменов':                      # РАСПИСАНИЕ ЗАНЯТИЙ или ЭКЗАМЕНОВ
        global choice 
        choice = message.text    # глобальная переменная для выбора между "расписанием экзхаменов" или "расписанием занятий"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("1 Курс")
        item2 = types.KeyboardButton("2 Курс")
        item3 = types.KeyboardButton("3 Курс")
        item4 = types.KeyboardButton("4 Курс")
        btn_exit = types.KeyboardButton("В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        bot.send_message(message.from_user.id,"Выберите курс", reply_markup = markup)
        bot.register_next_step_handler(message, tRas_tExm)

    if message.text == 'В главное меню':          # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())

@bot.message_handler(content_types=['text'])
def tRas_tExm(message):
    if message.text == '1 Курс' and choice == 'Расписание занятий':
        doc = open('document/table_default/1_kurs_raspisanie_zanyatiy.xlsx', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, tRas_tExm)
    elif message.text == '1 Курс' and choice == 'Расписание экзаменов':
        doc = open('document/table_exm/1_kurs_raspisanie_exams.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, tRas_tExm)        

    if message.text == '2 Курс' and choice == 'Расписание занятий':
        doc = open('document/table_default/2_kurs_raspisanie_zanyatiy.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, tRas_tExm)
    elif message.text == '2 Курс' and choice == 'Расписание экзаменов':
        doc = open('document/table_exm/2_kurs_raspisanie_exams.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, tRas_tExm) 

    if message.text == '3 Курс' and choice == 'Расписание занятий':
        doc = open('document/table_default/3_kurs_raspisanie_zanyatiy.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, tRas_tExm)
    elif message.text == '3 Курс' and choice == 'Расписание экзаменов':
        doc = open('document/table_exm/3_kurs_raspisanie_exams.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, tRas_tExm)          

    if message.text == '4 Курс' and choice == 'Расписание занятий':
        doc = open('document/table_default/4_kurs_raspisanie_zanyatiy.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, tRas_tExm)
    elif message.text == '4 Курс' and choice == 'Расписание экзаменов':
        doc = open('document/table_exm/4_kurs_raspisanie_exams.xls', 'rb')
        bot.send_document(message.from_user.id, doc)       
        bot.register_next_step_handler(message, tRas_tExm)

    if message.text == 'В главное меню':          # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())                            


@bot.message_handler(content_types=['text'])               # НАЖАТА КНОПКА "КОРПУСА"
def build(message):
    if message.text == 'В главное меню':          # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.я", reply_markup = back_to_main())
    else:
        name, address = choice_build (message)     # вызывается функция для выбора корпуса
        img = open(f'img/builds/{name.title()}', 'rb')
        bot.send_photo(message.from_user.id, img)           
        bot.send_message(message.chat.id, f'{address.title()}')
        bot.register_next_step_handler(message, build)


@bot.message_handler(content_types=['text'])      # НАЖАТА КНОПКА "ПОЛЕЗНЫЕ ССЫЛКИ"
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
        btn_exit = types.KeyboardButton("В главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, item7, btn_exit)
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
        btn_exit = types.KeyboardButton("В главное меню")
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9,  item10, btn_exit)
        bot.send_message(message.from_user.id,"Сайты для помощи студентам ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, useful_links)      

    if message.text == 'Спорт':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Отдел спорта ВолгГТУ")
        item2 = types.KeyboardButton("Студенческий спортивный клуб ВолгГТУ (Группа VK)")   
        btn_exit = types.KeyboardButton("В главное меню")
        markup.add(item1, item2, btn_exit)
        bot.send_message(message.from_user.id,"Сайты и группы, посвященные спорту ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, useful_links) 

    if message.text == 'Пароли и логины для DUMP':             # ОТСЫЛАЕТ КАРТИНКУ С ЛОГИНАМИ И ПАРОЛЯМИ ОТ DUMP.VSTU.RU
        img = open('img/table_dump_logins/parol_login_dump.jpg', 'rb')
        bot.send_photo(message.from_user.id, img)     
        bot.register_next_step_handler(message, website)

    if message.text == 'В главное меню':          # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())

@bot.message_handler(content_types=['text'])      # функция для вызова функции с выбором полезной ссылки ссылки
def useful_links(message):
    if message.text == 'В главное меню' or choice == 'В главное меню':          # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())
    else:
        link = choice_website(choice, message)
        bot.send_message(message.chat.id, link)
        bot.register_next_step_handler(message, useful_links)


@bot.message_handler(content_types=['text'])         # НАЖАТА КНОПКА "ОСНОВНЫЕ ПОДРАЗДЕЛЕНИЯ"
def osn_podrazdeleniya(message):
    if message.text == 'Деканат ФЭВТ':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Расписание и кабинет (Деканат ФЭВТ)")
        item2 = types.KeyboardButton("Группа VK (Деканат ФЭВТ)")
        item3 = types.KeyboardButton("Рейтинговая оценка системы знаний")
        btn_exit = types.KeyboardButton("В главное меню")
        markup.add(item1, item2, item3, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о деканате ФЭВТ", reply_markup = markup)
        bot.register_next_step_handler(message, decanat_FEVT)

    if message.text == 'Библиотека':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Расписание (Библиотека)")
        item2 = types.KeyboardButton("Группа VK (Библиотека)")
        item3 = types.KeyboardButton("Сайт (Библиотека)")
        btn_exit = types.KeyboardButton("В главное меню")
        markup.add(item1, item2, item3, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о библиотеке ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, library)   

    if message.text == 'Профком':    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Кабинет и расписание (Профком)")
        item2 = types.KeyboardButton("Группа VK (Профком)")
        item3 = types.KeyboardButton("Сайт (Профком)")
        btn_exit = types.KeyboardButton("В главное меню")
        markup.add(item1, item2, item3, btn_exit)
        bot.send_message(message.from_user.id,"Выберите какую информацию вы хотите получить о профкоме ВолгГТУ", reply_markup = markup)
        bot.register_next_step_handler(message, profkom)

    if message.text == 'В главное меню':          # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())        

@bot.message_handler(content_types=['text'])         # НАЖАТА КНОПКА "Деканат ФЭВТ"
def decanat_FEVT(message):
    if message.text == 'Расписание и кабинет (Деканат ФЭВТ)':
        img = open('img/decanat_FEVT/grafic_rabot.jpg', 'rb')
        bot.send_photo(message.from_user.id, img)        
        bot.register_next_step_handler(message, decanat_FEVT)

    if message.text == 'Группа VK (Деканат ФЭВТ)':
        bot.send_message(message.chat.id, 'https://vk.com/club193491114')
        bot.register_next_step_handler(message, decanat_FEVT)
    
    if message.text == 'Рейтинговая оценка системы знаний':
        img = open('img/decanat_FEVT/reyting_ocenka.jpg', 'rb')
        bot.send_photo(message.from_user.id, img)        
        bot.register_next_step_handler(message, decanat_FEVT)

    if message.text == 'В главное меню':          # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())

@bot.message_handler(content_types=['text'])         # НАЖАТА КНОПКА "Библиотека"
def library(message):  
    if message.text == 'Расписание (Библиотека)':
        bot.send_message(message.from_user.id, 'пн-пт 8.30-17.00 \n сб 9.00-16.00')
        bot.register_next_step_handler(message, library)

    if message.text == 'Группа VK (Библиотека)':
        bot.send_message(message.from_user.id, 'https://vk.com/library_vstu')
        bot.register_next_step_handler(message, library)

    if message.text == 'Сайт (Библиотека)':
        bot.send_message(message.from_user.id, 'http://library.vstu.ru/node/28')
        bot.register_next_step_handler(message, library)

    if message.text == 'В главное меню':          # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())

@bot.message_handler(content_types=['text'])         # НАЖАТА КНОПКА "Профком"
def profkom(message):  
    if message.text == 'Кабинет и расписание (Профком)':
        bot.send_message(message.from_user.id, ' Кабинет: ГУК - 147 \n пн-чт 8.30-17.00 \n пт 8.30-15.00')
        bot.register_next_step_handler(message, profkom)

    if message.text == 'Группа VK (Профком)':
        bot.send_message(message.from_user.id, 'https://vk.com/pksvstu')
        bot.register_next_step_handler(message, profkom)

    if message.text == 'Сайт (Профком)':
        bot.send_message(message.from_user.id, 'https://www.eseur.ru/volgograd/gosudarstvennogo_tehnicheskogo__universiteta/')
        bot.register_next_step_handler(message, profkom)

    if message.text == 'В главное меню':          # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main()) 


def choice_build(message):                         # функция для выбора корпуса
    if message.text == 'Высотный учебный корпус':
        name = 'Visotka.png'
        address = 'Высотный учебный корпус. Адрес: Волгоград, проспект им. Ленина, 28а'

    if message.text == 'Главный учебный корпус':
        name = 'GUK.png'
        address = 'Главный учебный корпус. Адрес: Волгоград, проспект им. Ленина, 28'

    if message.text == 'А учебный корпус':
        name = 'A_korpus.png'
        address = 'А учебный корпус. Адрес: Волгоград, Советская, 31'

    if message.text == 'Б учебный корпус':
        name = 'B_korpus.png'
        address = 'Б учебный корпус. Адрес: Волгоград, Советская, 29'

    if message.text == 'Тракторный учебный корпус':
        name = 'Traktorniy.png'
        address = 'Тракторный учебный корпус. Адрес: Волгоград, Дегтярёва, 2'

    if message.text == 'Кировский учебный корпус':
        name = 'Kirovskiy.png'
        address = 'Кировский учебный корпус. Адрес: Волгоград, Армавирская, 15'

    if message.text == 'Красноармейский учебный корпус':
        name = 'Krasnoarmeyskiy.png'
        address = 'Красноармейский учебный корпус. Адрес: Волгоград, проспект Столетова, 8'

    if message.text == 'В главное меню':          # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())          
    
    return name, address


def choice_website(choice_group, message):        # функция для выбора полезных ссылок
    choice_website = message.text    # переменная для перевода message в формат message.text

    if choice_group == 'Сайты ВолгГТУ':  # если выбрана "Сайты ВолгГТУ"
        if choice_website == 'edu':
            link = 'http://edu.vstu.ru/'
        if choice_website == 'eos2':
            link = 'https://eos2.vstu.ru/'      
        if choice_website == 'Рейтинг студента':
            link = 'https://www.vstu.ru/student/reyting-studenta/index.php?dep=fevt'
        if choice_website == 'Главная страница ВолгГТУ':
            link = 'https://www.vstu.ru/'
        if choice_website == 'DUMP - Хранилище':
            link = 'http://dump.vstu.ru/'   
        if choice_website== 'Библиотека':
            link = 'http://library.vstu.ru/'
        if choice_website == 'Деканат ФЭВТ (VK группа)':
            link = 'https://vk.com/club193491114'
    
    if choice_group == 'Вспомогательные':    # если выбрана "Вспомогательные"
        if choice_website == 'Diagrams.net':
            link = 'https://app.diagrams.net/'
        if choice_website == 'ERDPlus':
            link = 'https://erdplus.com/'    
        if choice_website == 'Iconfinder - картинки для приложений':
            link = 'https://www.iconfinder.com/'
        if choice_website == 'Online Color Picker':
            link = 'https://colorpicker.me/#4c063b'
        if choice_website == 'sistemas - картинки для приложений':
            link = 'https://icon-icons.com/ru/pack/sistemas/2104'   
        if choice_website == 'Антиплагиат':
            link = 'https://www.antiplagiat.ru/'
        if choice_website == 'Перевод двоичного кода в текст онлайн':
            link = 'https://allcalc.ru/node/1977'
        if choice_website == 'Решение СЛАУ онлайн':
            link = 'https://ru.onlinemschool.com/math/assistance/equation/gaus/'          
        if choice_website == 'Определитель матрицы онлайн':
            link = 'https://ru.onlinemschool.com/math/assistance/matrix/determinant/'
        if choice_website == 'GeoGebra':
            link = 'https://www.geogebra.org/'

    if choice_group == 'Спорт':    # если выбрана "Спорт"
        if choice_group == 'Спорт' and choice_website == 'Отдел спорта ВолгГТУ':
            link = 'https://www.vstu.ru/student/studencheskaya-zhizn/sportivnaya-deyatelnost/'
        if choice_group == 'Спорт' and choice_website == 'Студенческий спортивный клуб ВолгГТУ (Группа VK)':
            link = 'https://vk.com/public180881363'

    if choice_group == 'В главное меню' or choice_website == 'В главное меню' or message.text == 'В главное меню':  # ВЫПОЛНЯЕТСЯ ПЕРЕХОД В ГЛАВНОЕ МЕНЮ
        bot.send_message(message.from_user.id,"Здравствуйте, я - информационный бот VSTU для помощи студентам.", reply_markup = back_to_main())
    
    return link     





bot.polling(none_stop=True)