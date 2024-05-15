import json

from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.channels import GetParticipantsRequest


async def get_all_participants(client, channel):
    """Записывает json-файл с информацией о всех участниках канала/чата"""
    offset_user = 0  # номер участника, с которого начинается считывание
    limit_user = 100  # максимальное число записей, передаваемых за один раз

    all_participants = []  # список всех участников канала
    all_users_details = []  # список словарей с интересующими параметрами участников канала
    filter_user = ChannelParticipantsSearch('')

    while True:
        participants = await client(GetParticipantsRequest(channel, filter_user, offset_user, limit_user, hash=0))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset_user += len(participants.users)

    for participant in all_participants:
        all_users_details.append(
            {
                "id": participant.id,
                "first_name": participant.first_name,
                "last_name": participant.last_name,
                "user": participant.username,
                "phone": participant.phone,
                "is_bot": participant.bot
            }
        )

    with open(f'{channel}_channel_users.json', 'w', encoding='utf8') as outfile:
        json.dump(all_users_details, outfile, ensure_ascii=False)
