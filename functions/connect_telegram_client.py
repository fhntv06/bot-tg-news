import configparser
from telethon.sync import TelegramClient

from variables.common import path_to_config

# Считываем учетные данные
config = configparser.ConfigParser()
config.read(path_to_config, encoding="utf-8")

if not len(config.sections()):
    print(f'Не получены данные из config по пути: {path_to_config}!')
else:
    # Присваиваем значения внутренним переменным
    api_id = int(config['Telegram']['api_id'])
    api_hash = config['Telegram']['api_hash']
    username = config['Telegram']['username']

    client = TelegramClient(
        username,
        api_id,
        api_hash,
    )
