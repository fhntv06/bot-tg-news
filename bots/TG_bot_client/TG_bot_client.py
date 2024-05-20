from telethon import events
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
            all_messages = await get_all_messages(client, channel, 5, condition)  # метод для получения сообщений канала

            for message in all_messages:
                print('message ', message)
                # return
                await client.send_message(-1002093903863, f"Название: {message['message'][0:50]} ... : Просмотры: {message['views']}")  # отправка в канал -1002093903863


client.run_until_disconnected()

# with client:
#     client.loop.run_until_complete(main())
