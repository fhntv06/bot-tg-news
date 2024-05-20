import json
import os
import sys
import math

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


def set_ar_limit_numbers(total_count_limit):
    limit_msg_API = 100
    ar_limit_numbers = []

    fraction, integer = math.modf(total_count_limit / limit_msg_API)

    for i in range(int(integer)): ar_limit_numbers.append(limit_msg_API)
    if fraction: ar_limit_numbers.append(int(fraction * limit_msg_API))

    return ar_limit_numbers


async def get_all_messages(client, channel, total_count_limit, condition):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = set_ar_limit_numbers(total_count_limit)  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений

    for i in range(len(limit_msg)):
        history = await client(
            GetHistoryRequest(
                peer=channel,
                offset_id=offset_msg,
                offset_date=None,
                add_offset=0,
                limit=limit_msg[i],
                max_id=0,
                min_id=0,
                hash=0
            )
        )
        if not history.messages:
            break

        messages = history.messages

        for message in messages:
            if message.views is not None and message.views < condition:
                all_messages.append(message.to_dict())

        offset_msg = messages[len(messages) - 1].id

    dir_path = f'{sys.path[1]}/channels/{channel.username}/'
    file_name = f'{channel.username}_channel_messages.json'
    full_path = dir_path + file_name

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(full_path, 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)

    return all_messages
