from functions.connect_telegram_client import client
from functions.channel_participants_search import get_all_messages
from functions.get_participants_request import get_all_participants

client.start()


async def main():
    url = input("Введите ссылку на канал или чат: ")
    channel = await client.get_entity(url)
    await get_all_participants(client, channel)  # метод для получения участников канала (работает только если Вы админ)
    await get_all_messages(client, channel)  # метод для получения сообщений канала


with client:
    client.loop.run_until_complete(main())
