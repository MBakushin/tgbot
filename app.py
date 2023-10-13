import telebot
import os
from dotenv import load_dotenv
from config import common_valuta, all_valuta
from extensions import ExchangeRates, ConverterError


load_dotenv()
TOKEN = os.getenv("TOKEN")

if __name__ == "__main__":
    bot = telebot.TeleBot(TOKEN)


    @bot.message_handler(commands=["start", "help"])
    def echo_test(message: telebot.types.Message):
        text = """🤖 Чтобы начать работу введите 
команду в следующем формате:
<количество валюты> <исходная валюта> 
<валюта для конвертации>
Чтобы увидеть список распространенных валют - 
введите /valuta.
Чтобы увидеть список всех имеющихся валют - 
введите /allvaluta"""
        bot.reply_to(message, text)


    @bot.message_handler(commands=["allvaluta"])
    def get_all_values(message: telebot.types.Message):
        text = "Все доступные валюты:"
        for key, value in all_valuta.items():
            text = "\n".join((text, f"{key}: {value}"))
        bot.reply_to(message, text)


    @bot.message_handler(commands=["valuta"])
    def get_common_values(message: telebot.types.Message):
        text = "Распространенные валюты:"
        for key, value in common_valuta.items():
            text = "\n".join((text, f"{key}: {value}"))
        bot.reply_to(message, text)


    @bot.message_handler(content_types=["text"])
    def convert(message: telebot.types.Message):
        try:
            amount, base, quote = message.text.split()
            if not float(amount):
                raise ValueError
            elif base.upper() not in all_valuta.keys():
                raise ConverterError("Не могу определить исходную валюту\n")
            elif quote.upper() not in all_valuta.keys():
                raise ConverterError("Не могу определить валюту для конвертации\n")
        except ValueError:
            bot.send_message(message.chat.id, "Неверный формат данных\n"
                                              "Попробуйте снова")
        except ConverterError as e:
            bot.send_message(message.chat.id, f"{e}Попробуйте снова")
        else:
            converting = ExchangeRates().convert(quote, base, amount)
            bot.send_message(message.chat.id, converting or "Сервис недоступен")


    bot.polling(non_stop=True)
