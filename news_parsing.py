from time import sleep
import telebot
from bs4 import BeautifulSoup
import requests
from config.telegram_token import TOKEN


bot = telebot.TeleBot(TOKEN, parse_mode=None)
name_channel = '@здесь название канала'  # здесь указывается группа

HOST = "https://www.block-chain24.com"
URL = "https://www.block-chain24.com/news/novosti-kriptovalyutnyh-birzh"
HEADERS = {
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
    "accept": "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8" 
}
def get_html(url: str, params=' '):
    # это функция получает данные из сайта #
    return requests.get(url, headers=HEADERS, params=params)
html = get_html(URL, HEADERS)
new_list = {'title': None, 
            'image': None,
            'desc': None,
            'link': None,
            'data': None,
            }
old_list = {'title': None}
def get_content() -> list:
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find('div', class_='listitem clr')  # главный класс к которуму мы обращаемся
    title = items.find('div', class_='listitem__info').find('p', class_='listitem__title').text
    image = items.find('div', class_='listitem__img').find('img').get('src')
    link = HOST + items.find('p', class_='listitem__title').find('a').get('href')
    desc = items.find('div', class_='listitem__desc').text
    data = items.find('p', class_='listitem__published').text
    new_list['title'] = title
    new_list['image'] = image
    new_list['link'] = link
    new_list['desc'] = desc
    new_list['data'] = data

get_content()
old_list['title'] = new_list['title']

while True:
    get_content()
    if new_list['title'] != old_list['title']:
        bot.send_message(name_channel, f'''
        	🔥Новости криптовалютных бирж: {new_list['data']}\n
        	⚡{new_list['title']}\n
        	✍{new_list['desc']}\n
            ''')
        bot.send_photo(name_channel, photo=f'{new_list["image"]}', caption=new_list['link'])
        old_list['title'] = new_list['title']
        sleep(15)
    else:
        sleep(40)

	
