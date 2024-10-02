import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram import Bot
import requests
from xml.etree import ElementTree as ET

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

def get_currency_rates():
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    response.encoding = 'utf-8'
    xml_data = response.text
    root = ET.fromstring(xml_data)
    usd_rate = None
    eur_rate = None
    cny_rate = None

    for valute in root.findall('Valute'):
        if valute.find('CharCode').text == 'USD':
            usd_rate = float(valute.find('Value').text.replace(',', '.'))
        elif valute.find('CharCode').text == 'EUR':
            eur_rate = float(valute.find('Value').text.replace(',', '.'))
        elif valute.find('CharCode').text == 'CNY':
            cny_rate = float(valute.find('Value').text.replace(',', '.'))

    return usd_rate, eur_rate, cny_rate

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f"Добрый день, {user.first_name}! Как вас зовут?")

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.message.text
    usd_rate, eur_rate, cny_rate = get_currency_rates()
    if usd_rate is None:
        usd_rate = "Недоступен"
    if eur_rate is None:
        eur_rate = "Недоступен"
    if cny_rate is None:
        cny_rate = "Недоступен"
    await update.message.reply_text(
        f"Рад знакомству, {user_name}!\n"
        f"Курс доллара сегодня {usd_rate} руб.\n"
        f"Курс евро сегодня {eur_rate} руб.\n"
        f"Курс юаня сегодня {cny_rate} руб.\n"
    )

if __name__ == '__main__':
    token = "7701337825:AAHi_7k87UyMnWA0JryjmJqI6voBuNvr-Ic" 
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))
    application.run_polling()
