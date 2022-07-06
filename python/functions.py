from telebot import types
import mysql.connector
from connect import host, user, password, database
import connect  # подключение файла коннект для подключения к БД
import re
import time

mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database)

mycursor = mydb.cursor()

def about_help():                                                                      # феукция для вывода сообщения для помощи пользователю
    return "Я - информационный бот VSTU для помощи студентам ФЭВТ 1-4 курса.\n\n"\
        "Я умею следующее:\n\n ✅ могу выдать расписание занятий и экзаменов студентов ФЭВТ,\n\n"\
        " ✅ сохранять ваши заметки и напоминать о них,\n\n ✅ владею информацией, во сколько и в каком кабинете находится преподаватель САПР;\n\n"\
        " ✅ знаю где находятся все корпуса ВолгГТУ в Волггограде;\n\n ✅ подскажу что делать военнообязанным (или уже отслужившим) юношам;\n\n"\
        " ✅ расскажу какие виды стипендий бывают, а также о том, как их получить;\n\n ✅ могу подсказать, какие сайты или ресурсы будут полезны студенту ФЭВТ;\n\n"\
        " ✅ ведаю, информацией о деканате ФЭВТ, библиотеке и профкоме ВолгГТУ;\n\n ✅ могу рассказать о мероприятих, которые намечаются в ВолгГТУ в ближайшее время;\n\n"\
        " ✅ знаю когда и в каком кабинете у каждой группы ФЭВТ консультации.\n\n"\
        " ⁉️ чтобы начать общение с ботом VSTU, введите \"/start\" или выберите по кнопке \"меню\" слева, а затем нажмите на команду \"/start\""
        

def choice_build(message):                         # функция для выбора корпуса
    if message.text == 'Высотный учебный корпус':
        name = 'Visotka.png'
        address = 'Высотный учебный корпус. Адрес: Волгоград, проспект им. Ленина, 28а'

    elif message.text == 'Главный учебный корпус':
        name = 'GUK.png'
        address = 'Главный учебный корпус. Адрес: Волгоград, проспект им. Ленина, 28'

    elif message.text == 'А учебный корпус':
        name = 'A_korpus.png'
        address = 'А учебный корпус. Адрес: Волгоград, Советская, 31'

    elif message.text == 'Б учебный корпус':
        name = 'B_korpus.png'
        address = 'Б учебный корпус. Адрес: Волгоград, Советская, 29'

    elif message.text == 'Тракторный учебный корпус':
        name = 'Traktorniy.png'
        address = 'Тракторный учебный корпус. Адрес: Волгоград, Дегтярёва, 2'

    elif message.text == 'Кировский учебный корпус':
        name = 'Kirovskiy.png'
        address = 'Кировский учебный корпус. Адрес: Волгоград, Армавирская, 15'

    elif message.text == 'Красноармейский учебный корпус':
        name = 'Krasnoarmeyskiy.png'
        address = 'Красноармейский учебный корпус. Адрес: Волгоград, проспект Столетова, 8'

    else:
        name = 0
        address = 0         
    
    return name, address


def choice_website(choice_group, message):        # функция для выбора полезных ссылок
    choice_website = message.text    # переменная для перевода message в формат message.text

    if choice_group == '🎓 Сайты ВолгГТУ':  # если выбрана "Сайты ВолгГТУ"
        if choice_website == 'edu':
            link = 'http://edu.vstu.ru/'
        elif choice_website == 'eos2':
            link = 'https://eos2.vstu.ru/'      
        elif choice_website == 'Рейтинг студента':
            link = 'https://www.vstu.ru/student/reyting-studenta/index.php?dep=fevt'
        elif choice_website == 'Главная страница ВолгГТУ':
            link = 'https://www.vstu.ru/'
        elif choice_website == 'DUMP - Хранилище':
            link = 'http://dump.vstu.ru/'   
        elif choice_website== 'Библиотека':
            link = 'http://library.vstu.ru/'
        elif choice_website == 'Деканат ФЭВТ (VK группа)':
            link = 'https://vk.com/club193491114'
        else:
            link = 0
    
    elif choice_group == '🏖️ Вспомогательные':    # если выбрана "Вспомогательные"
        if choice_website == 'Diagrams.net':
            link = 'https://app.diagrams.net/'
        elif choice_website == 'ERDPlus':
            link = 'https://erdplus.com/'    
        elif choice_website == 'Iconfinder - картинки для приложений':
            link = 'https://www.iconfinder.com/'
        elif choice_website == 'Online Color Picker':
            link = 'https://colorpicker.me/#4c063b'
        elif choice_website == 'sistemas - картинки для приложений':
            link = 'https://icon-icons.com/ru/pack/sistemas/2104'   
        elif choice_website == 'Антиплагиат':
            link = 'https://www.antiplagiat.ru/'
        elif choice_website == 'Перевод двоичного кода в текст онлайн':
            link = 'https://allcalc.ru/node/1977'
        elif choice_website == 'Решение СЛАУ онлайн':
            link = 'https://ru.onlinemschool.com/math/assistance/equation/gaus/'          
        elif choice_website == 'Определитель матрицы онлайн':
            link = 'https://ru.onlinemschool.com/math/assistance/matrix/determinant/'
        elif choice_website == 'GeoGebra':
            link = 'https://www.geogebra.org/'
        else:
            link = 0

    elif choice_group == '🏆 Спорт':    # если выбрана "Спорт"
        if choice_group == '🏆 Спорт' and choice_website == 'Отдел спорта ВолгГТУ':
            link = 'https://www.vstu.ru/student/studencheskaya-zhizn/sportivnaya-deyatelnost/'
        elif choice_group == '🏆 Спорт' and choice_website == 'Студенческий спортивный клуб ВолгГТУ (Группа VK)':
            link = 'https://vk.com/public180881363'
        else:
            link = 0

    else:
        return 0
    
    return link     

def choice_osn_podrazdeleniya(choice_podrazdelenie, message):        # функция для выбора основных подразделений
    if choice_podrazdelenie == '📫 Деканат ФЭВТ':    # если выбрана "📫 Деканат ФЭВТ"
        if message.text == 'Расписание и кабинет (Деканат ФЭВТ)':
            info = '  Кабинет: В - 1207\nГрафик работы со студентами:\n\n пн-пт 11.00-12.30\n            13.00-15.00'

        elif message.text == 'Группа VK (Деканат ФЭВТ)':
            info = 'https://vk.com/club193491114'

        elif message.text == 'Рейтинговая оценка системы знаний':
            info = '  Оценки в зависимости от баллов:\n\n 5 - 90 - 100 баллов\n 4 - 76 - 89 баллов\n 3 - 61 - 75 баллов\n'\
                ' 2 - менее 60-ти баллов\n\n К итоговой аттестации допускаются\n студенты, набравшие по изучаемой\n дисциплине 40 - 60 баллов за семестр'
        else:
            info = 0

    elif choice_podrazdelenie == '📕 Библиотека':    # если выбрана "📕 Библиотека"
        if message.text == 'Расписание (Библиотека)':
            info = 'пн-пт 8.30-17.00 \n      сб 9.00-16.00'

        elif message.text == 'Группа VK (Библиотека)':
            info = 'https://vk.com/library_vstu'

        elif message.text == 'Сайт (Библиотека)':
            info = 'http://library.vstu.ru/node/28'

        else:
            info = 0    

    elif choice_podrazdelenie == '💸 Профком':    # если выбрана "💸 Профком"
        if message.text == 'Кабинет и расписание (Профком)':
            info = ' Кабинет: ГУК - 147 \n пн-чт 8.30-17.00 \n       пт 8.30-15.00'

        elif message.text == 'Группа VK (Профком)':
            info = 'https://vk.com/pksvstu'

        elif message.text == 'Сайт (Профком)':
            info = 'https://www.eseur.ru/volgograd/gosudarstvennogo_tehnicheskogo__universiteta/'

        else:
            info = 0

    elif choice_podrazdelenie == '🗿 2 Отдел':    # если выбрана "🗿 2 Отдел"
        if message.text == 'Кабинет и информация (2 отдел)':
            info = ' Адрес: Волгоград, пр. Ленина, 28\nКабинет: ГУК - 254 Б\n\nВ институте существует 2-отдел (2-е управление), одно из направлений которого'\
                ' – воинский учёт призывников и военнообязанных.\n\n ❗ При зачислении все студенты-юноши заполняют личную карточку.\n\n'\
                ' ❗ Все студенты в срок до 20 сентября должны подойти\nво 2-е отйдел с перечнем документов.\n\n ‼️ (для иногородних студентов)\n'\
                ' Иногородним студентам предварительно необходимо сняться с воинского учёта по месту жительства или прописки.'

        elif message.text == 'Какие документы необходимы? (2 отдел)':
            info = 'При себе необходимо иметь следущие документы (оригиналы!)\n\n ✳️ Приписное свидетельство (или военный билет)\n\n ✳️ Паспорт'

        elif message.text == 'Уже был там (2 отдел)':
            info = ' Всем студентам призывного возраста выдаются справки-приложения № 2 для оформления отсрочки от призыва на военную службу на период учёбы.\n'\
                ' Сами же справки-приложения № 2 необходимо предоставить в отдел военного комиссариата по г. Волгограду.\n\n ❗ (для иногородних студентов)\n'\
                ' В какой военный комиссариат и по какому адресу нести справки можно уточнить у работников 2-го отдела.\n\n'\
                ' ❗ при получении военного билета, уже после начала обучения в ВолгГТУ, студенту следует незамедлительно явиться во 2-е управление ВолгГТУ с военным билетом и паспортом.'

        else:
            info = 0

    elif choice_podrazdelenie == '💰 Стипендии':    # если выбрана "💰 Стипендии"
        if message.text == 'Какие виды стипендий бывают?':
            info = 'Всего существует два вида государственных стипендий:\n\n  1️⃣ Академическая,\n\n  2️⃣ Социальная.\n\n'\
                ' ⁉️ Однако, для особо заинтересованных студентов бывают еще и \"именные\" стипендии Президента РФ, Правительства РФ и иные стипендии.'\
                ' *(полный список можно уточнить в профкоме)\n\n ❗ Помимо этого есть еще и \"Социальная поддержка\"'

        elif message.text == 'Как получить академическую стипендию?':
            info = 'Государственная академическая стипендия может быть назначена студентам ТОЛЬКО по результатам сессии.\n\nУсловия получения академической стипендии:\n\n'\
                ' ❗ cтудент должен обучаться  только за счет федерального бюджета (бесплатно),\n\n ❗ студент должен вовремя закрыть сессию (!без пересдач) на оценки:'\
                ' \" 5️⃣ отлично\" и \" 4️⃣ хорошо\".\n\n ‼️ всем студентам 1 курса, зачисленным на бюджетные места в 1 семестре выплачивается академическая стипендия,\n\n'\
                ' ‼️ Размер стипендии в следующем семестре (после закрытия первого семестра и других последующих - БЕЗ ПЕРЕСДАЧ) будет зависеть от суммы баллов по всем предметам'\
                ' \"ЗАКРЫТОЙ\" текущей сессии!\n *(зависимость среднего балла от оценки можно посмотреть в этом чат-боте во вкладке:'\
                ' 🎓Основные подразделения ➡️ 📫Деканат ФЭВТ ➡️ Рейтинговая оценка системы знаний)'

        elif message.text == 'Кто имеет право на социальную стипендию?':
            info = 'Социальную стипендию могут получить следующие группы студентов:\n\n ✳️ студенты из числа детей-сирот и детей, оставшихся без попечения родителей,\n\n'\
                ' ✳️ студенты, признанные в установленном порядке инвалидами I и II групп, \n\n ✳️ студенты, являющиеся ветеранами боевых действий и инвалидами,\n\n'\
                ' ✳️ студенты, пострадавшие в результате аварии на Чернобыльской АЭС или других радиационных катастроф.'

        elif message.text == 'Как получить социальную стипендию?':
            info = 'Право получения государственной социальной стипендии имеет студент:\n\n ❗ обучающийся на бюджетной основе (бесплатно) по очной форме обучения,\n\n'\
                ' ❗ подавший справку в деканат факультета (методисту) для получения государственной социальной стипендии, выдаваемую органом социальной защиты населения'\
                ' по месту жительства.\n\n ‼️ чтобы получить \"справку для получения государственной социальной стипендии\" необходимо собрать справки: о составе семьи;'\
                ' о доходах всех членов семьи за последние 3 месяца.\n Эта справка представляется ежегодно, служит основанием для издания приказа и хранится в институте.'\
                ' Приём справок осуществляется до 5 числа каждого месяца!'

        elif message.text == 'Как получить социальную поддержку?':
            info = ' ❗ Социальная поддержка оказывается остро нуждающимся студентам на основании представленных заместителю декана факультета заявления и документов,'\
                ' подтверждающих необходимость в социальной поддержке.\n\n ❗ Социальная поддержка может выплачиваться только студентам дневного отделения,'\
                ' обучающимся за счет средств государственного бюджета (бесплатно).\n\n ❗ Студентам же, обучающимся за счет частичной или полной компенсации средств'\
                ' (платная форма обучения) выдача материальной помощи НЕ ПРОИЗВОДИТСЯ!'
        else:
            info = 0

    else:
        return 0

    return info  

def choice_tRas_tExm(choice_table, message):
    choice_kurs = message.text

    if choice_kurs == '1 Курс' and choice_table == '🗓️ Расписание занятий':      #  выбран 1 Курс
        way_to_table = 'document/table_default/1_kurs_raspisanie_zanyatiy.xlsx'

    elif choice_kurs == '1 Курс' and choice_table == '🗒️ Расписание экзаменов':
        way_to_table = 'document/table_exm/1_kurs_raspisanie_exams.xls'       

    elif choice_kurs == '2 Курс' and choice_table == '🗓️ Расписание занятий':      #  выбран 2 Курс
        way_to_table = 'document/table_default/2_kurs_raspisanie_zanyatiy.xls'

    elif choice_kurs == '2 Курс' and choice_table == '🗒️ Расписание экзаменов':
        way_to_table = 'document/table_exm/2_kurs_raspisanie_exams.xls'

    elif choice_kurs == '3 Курс' and choice_table == '🗓️ Расписание занятий':      #  выбран 3 Курс
        way_to_table = 'document/table_default/3_kurs_raspisanie_zanyatiy.xls'

    elif choice_kurs == '3 Курс' and choice_table == 'Расписание экзаменов':
        way_to_table = 'document/table_exm/3_kurs_raspisanie_exams.xls'        

    elif choice_kurs == '4 Курс' and choice_table == '🗓️ Расписание занятий':      #  выбран 4 Курс
        way_to_table = 'document/table_default/4_kurs_raspisanie_zanyatiy.xls'

    elif choice_kurs == '4 Курс' and choice_table == '🗒️ Расписание экзаменов':
        way_to_table = 'document/table_exm/4_kurs_raspisanie_exams.xls'

    else:
        return 0

    return way_to_table 


def choice_day_of_week(message):                         # функция для выбора дня недели
    if message.text == 'Понедельник':
        name = 'пн'

    elif message.text == 'Вторник':
        name = 'вт'

    elif message.text == 'Среда':
        name = 'ср'

    elif message.text == 'Четверг':
        name = 'чт'

    elif message.text == 'Пятница':
        name = 'пт'

    elif message.text == 'Суббота':
        name = 'сб'

    else:
        name = 0
   
    return name

def choice_parity_of_week(message):                         # функция для выбора четности недели
    if message.text == '1️⃣ Неделя':
        parity = '1'

    elif message.text == '2️⃣ Неделя':
        parity = '2'

    else:
        parity = 0
   
    return parity

def teacher_name_search(message):          # ПОИСК НУЖНОГО ПРЕПОДАВАТЕЛЯ
    try:
        sql = "SELECT teacher_fio FROM _teachers where teacher_fio = "+"\""+message.text+"\""
        mycursor.execute(sql)
        exist = mycursor.fetchall()
        
        if len(exist) == 1:
            return 1
        else:
            return 0

    except:
        return 0