import telebot
import mysql.connector
import random
import datetime
BOT_TOKEN = "5581837086:AAFqDJgaaDop64v4cHA7HehlL08RNh-dTFU"

bot = telebot.TeleBot(BOT_TOKEN)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="telegrambot_db"
)

mycursor = mydb.cursor()

@bot.message_handler(content_types=['text'])
def handle(message):
    if message.text == '/about':
        bot.send_message(message.from_user.id, 'Hi, I\'m netrapsystembot')
    if  message.text == '/random':
        bot.send_message(message.from_user.id, random.randint(0,9))
    if  message.text == '/time':
        bot.send_message(message.from_user.id, str(datetime.datetime.now()))
    if  message.text == '/sessions':
        mycursor.execute('SELECT image FROM addresses')
        photos = mycursor.fetchone()
        for photo in photos:
            ph = photo[1]
        bot.send_photo(message.from_user.id, open(photo, 'rb'))

bot.polling(none_stop=True)