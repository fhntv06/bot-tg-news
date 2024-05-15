import requests
from bs4 import BeautifulSoup
import telebot
import time

token = '6448324107:AAGWD5q9mrD7Ce0NcJJSJJ063E1CCOlm11k'
id_channel = '@test_news_parse'
bot = telebot.TeleBot(token)


def parser(back_post_id):
    page = requests.get('https://habr.com/ru/search/?q=python&target_type=posts&order=relevance')
    soup = BeautifulSoup(page.content, 'html.parser')

    post = soup.find('article', class_='tm-articles-list__item')
    post_id = post['id']

    if post_id != back_post_id:
        title = soup.find('h2', class_='tm-title tm-title_h2').text.strip()
        url = soup.find('a', class_='tm-title__link', href=True)['href'].strip()

        return f'{title}\n\nhttps://habr.com{url}', post_id
    else:
        return None, post_id


@bot.message_handler(content_types=['text'])
def commands(message):
    if message.text == 'Старт':
        back_post_id = ''

        while True:
            post_text = parser(back_post_id)

            if post_text[0] is not None:
                back_post_id = post_text[1]
                print('Новый пост ', post_text)
                bot.send_message(id_channel, post_text)
            else:
                print('Новых постов нет!')
                bot.send_message(id_channel, 'Новых постов нет!')

            time.sleep(10)


bot.polling()
