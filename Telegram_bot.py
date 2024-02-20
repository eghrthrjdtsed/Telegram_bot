import telebot
import requests
import json

films = []
API_URL = 'https://7012.deeppavlov.ai/model'

API_TOKEN = 'your token'
bot = telebot.TeleBot(API_TOKEN)
API_KEY = 'your token openweathermap'


def get_weather(city):
    global API_KEY
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data.get('cod') == 200:
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f'Погода в {city}: {weather}, Температура: {temperature}°C'
    else:
        return 'Извините, не удалось получить информацию о погоде.'


@bot.message_handler(commands=['start'])
def start_message(message):
    films.extend(["Матрица", "Солярис", "Властелин колец", "Техасская резня бензопилой", "Санта Барбара"])
    bot.send_message(message.chat.id, "Фильмотека была загружена по умолчанию!")


@bot.message_handler(commands=['all'])
def show_all(message):
    if films:
        bot.send_message(message.chat.id, "Вот список фильмов")
        bot.send_message(message.chat.id, ", ".join(films))
    else:
        bot.send_message(message.chat.id, "Фильмотека пуста")


@bot.message_handler(commands=['save'])
def save_all(message):
    if films:
        with open("films.json", "w", encoding="utf-8") as fh:
            json.dump(films, fh, ensure_ascii=False)
        bot.send_message(message.chat.id, "Наша фильмотека была успешно сохранена в файле films.json")
    else:
        bot.send_message(message.chat.id, "Фильмотека пуста")


@bot.message_handler(commands=['wiki'])
def wiki(message):
    quest = " ".join(message.text.split()[1:])
    data = {'question_raw': [quest]}
    try:
        res = requests.post(API_URL, json=data).json()
        bot.send_message(message.chat.id, res)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if 'дела' in message.text.lower():
        bot.send_message(message.chat.id, "Дела у меня хорошо, как сам?")


@bot.message_handler(commands=['add'])
def add_film(message):
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "Пожалуйста, укажите название фильма")
    else:
        film_name = " ".join(message.text.split()[1:])
        films.append(film_name)
        bot.send_message(message.chat.id, "Фильм успешно добавлен!")


@bot.message_handler(commands=['remove'])
def remove_film(message):
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "Пожалуйста, укажите название фильма")
    else:
        film_name = " ".join(message.text.split()[1:])
        if film_name in films:
            films.remove(film_name)
            bot.send_message(message.chat.id, "Фильм успешно удален!")
        else:
            bot.send_message(message.chat.id, "Такого фильма нет")


@bot.message_handler(commands=['weather'])
def get_current_weather(message):
    try:
        city = message.text.split()[1]
        weather_info = get_weather(city)
        bot.send_message(message.chat.id, weather_info)
    except IndexError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите название города!")


bot.polling()
