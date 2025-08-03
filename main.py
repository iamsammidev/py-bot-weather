import telebot
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# BOT
bot_token = os.getenv("BOTTOKEN")
bot = telebot.TeleBot(bot_token)

# WEATHER
weather_token = os.getenv("WTOKEN")

# ACCESS LIST
data_string = os.getenv("ACC", "")
acl = []
try:
    acl = [int(x) for x in data_string.split(',') if x.strip()]
except ValueError as e:
    print("Invalid value in ACC:", e)
    acl = []

access_list = acl
print("acl", data_string)
print("list", access_list)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, рад тебя видеть! Напиши название города.')


@bot.message_handler(commands=['id'])
def start(message):
    id = message.chat.id
    name = message.chat.first_name
    bot.send_message(message.chat.id, f'{name}, Ваш идентификатор {id}')



@bot.message_handler(content_types=['text'])
def get_weather(message):
    id = message.chat.id
    if id not in access_list:
        bot.reply_to(message, 'У вас нет прав доступа')
        return

    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Сейчас погода: {temp}')

        # image = 'sunny.jpg' if temp > 5.0 else 'sun.png'
        if temp > 5.0:
            image = 'sunny.jpg'
        else:
            image = 'sun.png'

        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Город указан не верно')


if __name__ == '__main__':
    bot.polling(none_stop=True)
