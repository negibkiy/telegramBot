from email import message
from telebot import types

def main_menu(message): 
    if message.text == '💼 Мероприятия':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Войти в аккаунт")
        item2 = types.KeyboardButton("Зарегистрироваться")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, btn_exit)

    if message.text == '🏢 Консультации':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Войти в аккаунт")
        item2 = types.KeyboardButton("Зарегистрироваться")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, btn_exit)

    if message.text == '📝 Заметки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Войти в аккаунт")
        item2 = types.KeyboardButton("Зарегистрироваться")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, btn_exit)

    elif message.text == '🎓 Основные подразделения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("📫 Деканат ФЭВТ")
        item2 = types.KeyboardButton("📕 Библиотека")
        item3 = types.KeyboardButton("💸 Профком")
        item4 = types.KeyboardButton("🗿 2 Отдел")
        item5 = types.KeyboardButton("💰 Стипендии")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, item5, btn_exit)        

    elif message.text == '📂 Полезные ссылки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("🎓 Сайты ВолгГТУ")
        item2 = types.KeyboardButton("🏖️ Вспомогательные")
        item3 = types.KeyboardButton("🏆 Спорт")
        item4 = types.KeyboardButton("📚 Пароли и логины для DUMP")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)

    elif  message.text == '🏛️ Корпуса':                               
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

    elif message.text == '📅 Расписание':                          
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("📋 Расписание преподавателя")
        item2 = types.KeyboardButton("🗒️ Расписание экзаменов")
        item3 = types.KeyboardButton("🗓️ Расписание занятий")
        item4 = types.KeyboardButton("🔔 Расписание звонков")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)

    return markup


def back_to_main():                                     # ФУНКЦИЯ ДЛЯ ВЫЗОВА ГЛАВНОГО МЕНЮ
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("💼 Мероприятия")
    item2 = types.KeyboardButton("🏢 Консультации")
    item3 = types.KeyboardButton("📝 Заметки")
    item4= types.KeyboardButton("🎓 Основные подразделения")
    item5 = types.KeyboardButton("📂 Полезные ссылки")
    item6 = types.KeyboardButton("🏛️ Корпуса") 
    item7 = types.KeyboardButton("📅 Расписание")
    markup.add(item1, item2, item3, item4, item5, item6, item7)
    
    return markup

def one_step_back(booling_word, message):
    if booling_word == '📅 Расписание':                            # ВЫБОР РАСПИСАНИЯ 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("📋 Расписание преподавателя")
        item2 = types.KeyboardButton("🗒️ Расписание экзаменов")
        item3 = types.KeyboardButton("🗓️ Расписание занятий")
        item4 = types.KeyboardButton("🔔 Расписание звонков")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        notification = "📅 Расписание"
    
    if booling_word == '📂 Полезные ссылки':                       # ВЫБОР ПОЛЕЗНЫХ ССЫЛОК
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("🎓 Сайты ВолгГТУ")
        item2 = types.KeyboardButton("🏖️ Вспомогательные")
        item3 = types.KeyboardButton("🏆 Спорт")
        item4 = types.KeyboardButton("📚 Пароли и логины для DUMP")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, btn_exit)
        notification = "📂 Полезные ссылки"      
    
    if booling_word == '🎓 Основные подразделения':                # ВЫБОР ОСНОВНЫХ ПОДРАЗДЕЛЕНИЙ
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("📫 Деканат ФЭВТ")
        item2 = types.KeyboardButton("📕 Библиотека")
        item3 = types.KeyboardButton("💸 Профком")
        item4 = types.KeyboardButton("🗿 2 Отдел")
        item5 = types.KeyboardButton("💰 Стипендии")
        btn_exit = types.KeyboardButton("⬆️ В главное меню")
        markup.add(item1, item2, item3, item4, item5, btn_exit)
        notification = "🎓 Основные подразделения"

    return markup, notification