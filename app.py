import telebot
from telebot import types
from config import keys, TOKEN
from extensions import APIException, CryptoConverter



bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/start")
    item2 = types.KeyboardButton("/help")
    item3 = types.KeyboardButton("/values")

    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Привет! Я CryptoDrahmatullinBot1 - конвертер валют. "\
    "\nЯ могу провести конвертацию валюты, для этого Вам необходимо ввести: "\
    '\n- "Название валюты, цену которой Вы хотите узнать"' \
    '\n- "Название валюты в которую нужно перевести"' \
    '\n- "Количество переводимой валюты" '\
    '\nПример: Доллар рубль 1 ' \
    "\nПоказать список доступных валют через команду /values " \
    "\nНапомнить, что я могу через команду /help .", reply_markup=markup)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) > 3:
            raise APIException('Слишком много параметров')
        if len(values) < 3:
            raise APIException('Введите количество переводимой валюты')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Произошла ошибка!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {float(total_base)*float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
