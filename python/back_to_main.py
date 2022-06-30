from email import message
import telebot
import mysql.connector
from connect import host, user, password, database
from telebot import types
import bot

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