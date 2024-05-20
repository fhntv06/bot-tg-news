from telethon import events
import sys
import os
from functions.connect_telegram_client import client
from functions.channel_participants_search import get_all_messages
from functions.get_participants_request import get_all_participants

client.start()

# url = input("Введите ссылку на канал или чат: ")

channels = {
    # 'https://t.me/Universal_Chronicles': 8000,
    'https://t.me/vseoblemluchi_obzor': 6000,
    # 'https://t.me/oreol_beskraev': 9000,
    # 'https://t.me/Panoptic_Planet': 8000,
    # 'https://t.me/cosmic_idea': 8000,
    # 'https://t.me/khameleon77': 700,
    # 'https://t.me/infinite_tapestry': 2000,
    # 'https://t.me/incomegalaxy': 6000,
    # 'https://t.me/cosmic_kaleidoscope': 9000,
    # 'https://t.me/global_vpechat': 8000,
    # 'https://t.me/hypekeeper': 9000,
}


@client.on(events.NewMessage(-1002093903863))
async def send_message(event):
    print(event.message.message)
    if event.message.message == 'get stats':
        print('command get stats')
        # работает!
        # можно тут запускать код -> получить название и просмотры -> пересылать в forward_messages
        for url, condition in channels.items():
            print(url, condition)
            channel = await client.get_entity(url)
            # await get_all_participants(client, channel)  # метод для получения участников канала (работает только если Вы админ)
            all_messages = await get_all_messages(client, channel, 2, condition)  # метод для получения сообщений канала

            # srtMessage = '' # отправка сообщения в канал '@test_news_parse'
            file_name = f'{channel.username}.txt'
            full_path = f'{sys.path[1]}/channels/{channel.username}/' + file_name

            for message in all_messages:
                with open(full_path, "a", encoding="utf-8") as file:
                    file.write(f"Id: {message['id']}\r\n")
                    file.write(f"Название канала: {message['message'][0:50]} ...\r\n")
                    file.write(f"Просмотры: {message['views']}\r\n")
                    file.write(f"Ссылка на канал: {message['entities'][0]['url']}\r\n\n")

                # отправка сообщения в канал '@test_news_parse'
                # srtMessage += f"Id: {message['id']}\r\n"
                # srtMessage += f"Название: {message['message'][0:50]} ...;\r\n"
                # srtMessage += f"Просмотры: {message['views']}\r\n"
                # srtMessage += f"Ссылка: {message['entities'][0]['url']}\r\n\n"

            if not os.path.exists(full_path):
                print(f"Файл {file_name} не создан!")
            else:
                print(f"Файл {file_name} успешно создан!")

            await client.send_file('@test_news_parse', full_path)

            print(f"Файл {file_name} успешно отправлен!")

            # await client.send_message('@test_news_parse', srtMessage)  # отправка сообщения в канал '@test_news_parse'


client.run_until_disconnected()

# with client:
#     client.loop.run_until_complete(main())
