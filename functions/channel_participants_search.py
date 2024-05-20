import json
import os
import sys

# для корректного переноса времени сообщений в json
from datetime import datetime

from telethon.tl.functions.messages import GetHistoryRequest


class DateTimeEncoder(json.JSONEncoder):
    """Класс для сериализации записи дат в JSON"""

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)


async def get_all_messages(client, channel, total_count_limit, condition):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 100 if total_count_limit >= 100 else total_count_limit  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений

    while True:
        if len(all_messages) >= total_count_limit - 1:
            break

        history = await client(
            GetHistoryRequest(
                peer=channel,
                offset_id=offset_msg,
                offset_date=None,
                add_offset=0,
                limit=limit_msg,
                max_id=0,
                min_id=0,
                hash=0
            )
        )
        if not history.messages:
            break

        messages = history.messages
        len(messages)

        for message in messages:
            if message.views is not None and message.views < condition:
                all_messages.append(message.to_dict())

        offset_msg = messages[len(messages) - 1].id

    len(all_messages)

    dir_path = f'{sys.path[1]}/channels/{channel.username}/'
    file_name = f'{channel.username}_channel_messages.json'
    full_path = dir_path + file_name

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(full_path, 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)

    return all_messages
