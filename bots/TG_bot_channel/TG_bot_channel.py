import telebot
import json
import subprocess

from variables.common import path_to_channels_jsons

token = '6448324107:AAGWD5q9mrD7Ce0NcJJSJJ063E1CCOlm11k' // revoke

bot = telebot.TeleBot(token)


def collect_posts(channel):
    with open(f'{path_to_channels_jsons + channel}.txt', 'w') as file:
        file = file.readline()

    posts = []
    for n, line in enumerate(file):
        file[n] = json.loads(file[n])
        links = [link for link in file[n]['outlinks'] if link != channel]
        p = f"{file[n]['content']}\n\n" + '\n'.join(links)
        posts.append(p)
    return posts


def upload_posts(num_posts, channel):
    command = f'snscrape --max-result {num_posts} --jsonl telegram-channel {channel} > {path_to_channels_jsons + channel}.txt'
    subprocess.run(command, shell=True)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
    "Напиши: \n1. Название канала, откуда выгрузить\n2. Сколько последних постов выгрузить\n3. куда "
         "выгрузить\n\nПример ввода:\n `other_channel 10 my_channel` "
    )


@bot.message_handler(content_types=['text'])
def set_process(message):
    try:
        channel, num_posts, target_channel = str(message.text).split()

        posts = collect_posts(channel)

        while posts:
            bot.send_message(target_channel, posts.pop())

        bot.reply_to(message, 'Отлично, пересылка завершена')

    except:
        bot.reply_to(message, 'Неправильный формат. Нажми /start, чтобы увидеть правильный формат.')


if __name__ == '__main__':
    bot.polling()
