import telebot
import sqlite3
BOT_TOKEN = "5581837086:AAFqDJgaaDop64v4cHA7HehlL08RNh-dTFU"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=[start])
def send_welcome