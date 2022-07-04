from telebot import types

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
    
    elif choice_group == '🏖️ Вспомогательные':    # если выбрана "Вспомогательные"
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

    elif choice_group == '🏆 Спорт':    # если выбрана "Спорт"
        if choice_group == '🏆 Спорт' and choice_website == 'Отдел спорта ВолгГТУ':
            link = 'https://www.vstu.ru/student/studencheskaya-zhizn/sportivnaya-deyatelnost/'
        if choice_group == '🏆 Спорт' and choice_website == 'Студенческий спортивный клуб ВолгГТУ (Группа VK)':
            link = 'https://vk.com/public180881363'

    else:
        return 0
    
    return link     

def choice_osn_podrazdeleniya(choice_podrazdelenie, message):        # функция для выбора основных подразделений
    choice_info = message.text

    if choice_podrazdelenie == '📫 Деканат ФЭВТ':    # если выбрана "📫 Деканат ФЭВТ"
        if message.text == 'Расписание и кабинет (Деканат ФЭВТ)':
            info = '  Кабинет: В - 1207\nГрафик работы со студентами:\n\n пн-пт 11.00-12.30\n            13.00-15.00'
        if message.text == 'Группа VK (Деканат ФЭВТ)':
            info = 'https://vk.com/club193491114'
        if message.text == 'Рейтинговая оценка системы знаний':
            info = '  Оценки в зависимости от баллов:\n\n 5 - 90 - 100 баллов\n 4 - 76 - 89 баллов\n 3 - 61 - 75 баллов\n 2 - менее 60-ти баллов\n\n К итоговой аттестации допускаются\n студенты, набравшие по изучаемой\n дисциплине 40 - 60 баллов за семестр'

    elif choice_podrazdelenie == '📕 Библиотека':    # если выбрана "📕 Библиотека"
        if message.text == 'Расписание (Библиотека)':
            info = 'пн-пт 8.30-17.00 \n      сб 9.00-16.00'
        if message.text == 'Группа VK (Библиотека)':
            info = 'https://vk.com/library_vstu'
        if message.text == 'Сайт (Библиотека)':
            info = 'http://library.vstu.ru/node/28'

    elif choice_podrazdelenie == '💸 Профком':    # если выбрана "💸 Профком"
        if message.text == 'Кабинет и расписание (Профком)':
            info = ' Кабинет: ГУК - 147 \n пн-чт 8.30-17.00 \n       пт 8.30-15.00'
        if message.text == 'Группа VK (Профком)':
            info = 'https://vk.com/pksvstu'
        if message.text == 'Сайт (Профком)':
            info = 'https://www.eseur.ru/volgograd/gosudarstvennogo_tehnicheskogo__universiteta/'

    elif choice_podrazdelenie == '🗿 2 Отдел':    # если выбрана "🗿 2 Отдел"
        if message.text == 'Кабинет и информация (2 отдел)':
            info = ' Адрес: Волгоград, пр. Ленина, 28\nКабинет: ГУК - 254 Б\n\nВ институте существует 2-отдел (2-е управление), одно из направлений которого – воинский учёт призывников и военнообязанных.\n\n ❗ При зачислении все студенты-юноши заполняют личную карточку.\n\n ❗ Все студенты в срок до 20 сентября должны подойти\nво 2-е отйдел с перечнем документов.\n\n ‼️ (для иногородних студентов)\n Иногородним студентам предварительно необходимо сняться с воинского учёта по месту жительства или прописки.'
        if message.text == 'Какие документы необходимы? (2 отдел)':
            info = 'При себе необходимо иметь следущие документы (оригиналы!)\n\n ✳️ Приписное свидетельство (или военный билет)\n\n ✳️ Паспорт'
        if message.text == 'Уже был там (2 отдел)':
            info = ' Всем студентам призывного возраста выдаются справки-приложения № 2 для оформления отсрочки от призыва на военную службу на период учёбы.\n Сами же справки-приложения № 2 необходимо предоставить в отдел военного комиссариата по г. Волгограду.\n\n ❗ (для иногородних студентов)\nВ какой военный комиссариат и по какому адресу нести справки можно уточнить у работников 2-го отдела.'

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
