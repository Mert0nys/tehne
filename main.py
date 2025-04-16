from telebot import TeleBot
import pandas as pd
from database import insert
from parser import parse_price

BOT_TOKEN = "7948451831:AAH5zxEcHCaM3hDZZ_X1ogvf3GXWREnyZb0"
bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Пришли мне Excel файл с данными о зюзюбликах!")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open('data.xlsx', 'wb') as new_file:
        new_file.write(downloaded_file)

    df = pd.read_excel('data.xlsx')
    bot.send_message(message.chat.id, f"Загруженные данные:\n{df.to_string()}")

    required_columns = ['url', 'xpath', 'title']
    if not all(column in df.columns for column in required_columns):
        bot.send_message(message.chat.id, "Ошибка: отсутствуют необходимые столбцы в загруженном файле.")
        return

    for index, row in df.iterrows():
        try:
            price = parse_price(row['url'], row['xpath'])
            if price is not None: 
                insert((row['title'], row['url'], row['xpath'], price))  
            else:
                bot.send_message(message.chat.id, f"Не удалось получить цену для строки {index + 1}.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка при обработке строки {index + 1}: {str(e)}")

if __name__ == "__main__":
    bot.polling(none_stop=True)
