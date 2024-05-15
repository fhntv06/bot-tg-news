import configparser
from telethon.sync import TelegramClient

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("../files/config.ini")

# Присваиваем значения внутренним переменным
api_id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(
    username,
    api_id,
    api_hash,
)

client.start()
