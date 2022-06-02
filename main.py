import time #Импортируем библиотеки
from threading import Thread
import telebot
from telebot import types

bot = telebot.TeleBot('5335946242:AAHmK64UfoUE-hV_2NknncTvYIwNyoAHckQ') # мой бот(токен)
#создаем словарь, где ключ - id пользователя, а значения - словарь данных о пользователе
#создаем хэндлер для команды старта и кнопки "начать"
users = {}

@bot.message_handler(commands=['start'])
def launch_window_output(message):
    keyboard = types.InlineKeyboardMarkup()
    creating_a_launch_button = types.InlineKeyboardButton(text='Запустить приложение', callback_data='START')
    keyboard.add(creating_a_launch_button)
    bot.send_message(message.chat.id, f'''Привет, {str(message.chat.first_name)}! ''', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda  call: True)
def getting_started(call):
    if call.data == 'START':
        bot.send_message(call.message.chat.id, 'какое сообщение необходимо напомнить??')

@bot.message_handler(content_types=['text'])
def reminder_message(message):#функция для получения сообщения от пользователя
    sms = message.text
    chat_id = message.chat.id
    answer = f'{str(message.chat.first_name)}. введите время в минутах, через сколько вам напомнить?'
    bot.send_message(message.chat.id, text=answer)
    bot.register_next_step_handler(message, getting_data)
    users[chat_id] = [sms]

def getting_data(message):#функция для получения времени
    time_through = message.text
    chat_id = message.chat.id
    users[chat_id].insert(1, time_through)
    # при вводе времени не в цифрах вывести это сообщение, иначе не выводить
    while time_through.isdigit() != True:
        bot.send_message(message.chat.id, 'Кажется что-то пошло не так')
        bot.register_next_step_handler(message, getting_data)
        users[chat_id].pop()
        break
    else:
        message_output(message)

def message_output(message):
    chat_id = message.chat.id
    time_through = users[chat_id][1]
    sms = users[chat_id][0]
    time.sleep(int(time_through)*60)#установка времени ответа
    bot.send_message(message.chat.id, text=f'Напоминаю что - : {sms}')

bot.polling(none_stop=True, interval=0)