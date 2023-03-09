import telebot
from telebot import types
from  extensions import Converter, ApiExeption
from nbv import *

conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
buttons = []
for i in keys.keys():
    buttons.append(types.KeyboardButton(i.capitalize()))

conv_markup.add(*buttons)

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу,\
 введите команду боту в следующем формате: /convert '
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i ))
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def convert(message: telebot.types.Message):
    text = 'Выберите валюту,из которой будете конвертировать'
    bot.send_message(message.chat.id, text, reply_markup=conv_markup)
    bot.register_next_step_handler(message, base_handler)
def base_handler(message: telebot.types.Message):
    base = message.text
    text = 'Выберите валюту,в которую будете конвертировать'
    bot.send_message(message.chat.id, text, reply_markup=conv_markup)
    bot.register_next_step_handler(message, quote_handler, base)
def quote_handler(message: telebot.types.Message, base):
    quote = message.text
    text = 'напишите количество конвертируемой валюты'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)
def amount_handler(message: telebot.types.Message, quote, base):
    amount = message.text
    try:
        priсe = Converter.get_price(base, quote, amount)
    except ApiExeption as e :
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n{e} ')
    else:
        text = f' Результат конвертации : {priсe}'
        bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=["text"])
def start_message(message):
    bot.send_message(message.chat.id, 'Нажмите на < /convert >')



bot.polling()


