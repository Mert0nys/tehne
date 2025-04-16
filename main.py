from telebot import TeleBot
import pandas as pd
from database import insert
from parser import parse_price
from io import BytesIO

BOT_TOKEN = "7948451831:AAH5zxEcHCaM3hDZZ_X1ogvf3GXWREnyZb0"
bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Пришли мне Excel файл с данными о зюзюбликах!")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    excel_file = BytesIO(downloaded_file)
    
    try:
        df = pd.read_excel(excel_file)

        required_columns = ['url', 'xpath', 'title']
        if not all(column in df.columns for column in required_columns):
            bot.send_message(message.chat.id, "Ошибка: отсутствуют необходимые столбцы в загруженном файле.")
            return

        # Получаем последнюю строку
        last_row = df.iloc[-1]
        last_row_message = f"*Последнее добавление:*\n\n*Title:* {last_row['title']}\n*URL:* {last_row['url']}\n*XPath:* {last_row['xpath']}"

        bot.send_message(message.chat.id, last_row_message, parse_mode='Markdown')

        # Обработка последней строки для получения цены и вставки в базу данных
        try:
            price = parse_price(last_row['url'], last_row['xpath'])
            if price is not None: 
                insert((last_row['title'], last_row['url'], last_row['xpath'], price))  
            else:
                bot.send_message(message.chat.id, "Не удалось получить цену для последнего добавления.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка при обработке последней строки: {str(e)}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при чтении файла: {str(e)}")

if __name__ == "__main__":
    bot.polling(none_stop=True)
