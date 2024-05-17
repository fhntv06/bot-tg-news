from functions.connect_telegram_client import client
from functions.channel_participants_search import get_all_messages
from functions.get_participants_request import get_all_participants

client.start()


async def main():
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

    for url, condition in channels.items():
        print(url, condition)
        channel = await client.get_entity(url)
        # await get_all_participants(client, channel)  # метод для получения участников канала (работает только если Вы админ)
        await get_all_messages(client, channel, 5, condition)  # метод для получения сообщений канала


with client:
    client.loop.run_until_complete(main())


# массив каналов


# получать 150 последних постов
# сортировать последние посты по заданному числу просмотров