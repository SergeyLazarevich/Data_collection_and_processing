#Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. 
#Для парсинга использовать XPath. Структура данных должна содержать:
#название источника;
#наименование новости;
#ссылку на новость;
#дата публикации.
#Сложить собранные данные в БД

from lxml import html
import requests
from dateutil.parser import parse
from pymongo import MongoClient
import hashlib

#Спарсим страницу с 'https://lenta.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/91.0.4472.135 YaBrowser/21.6.3.757 Yowser/2.5 Safari/537.36'}
main_link = 'https://lenta.ru/'
response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)
news_1 = dom.xpath('//div[@class="span8 js-main__content"]//div[@class="item"]')
news_2 = dom.xpath('//div[@class="item news b-tabloid__topic_news"]')
news_list = []

# Обработаем результат
for item in news_1:
    data = {}
    data['source'] = main_link
    data['text'] = item.xpath('.//a/text()')[0]
    data['link'] = f"{main_link}{item.xpath('.//a/@href')[0]}"
    data['time'] = parse(item.xpath('.//a/time/text()')[0])
    data['_id'] = hashlib.sha1(str(data).encode()).hexdigest()
    news_list.append(data)

for item in news_2:
    data = {}
    data['source'] = main_link
    data['text'] = item.xpath('.//h3/text()')[0]
    data['link'] = f"{main_link}{item.xpath('.//a/@href')[0]}"
    data['time'] = parse(item.xpath('.//span[@class="time"]/text()')[0])
    data['_id'] = hashlib.sha1(str(data).encode()).hexdigest()
    news_list.append(data)

#Сложим собранные данные в БД
client = MongoClient('localhost', 27017)
db = client['news_database']
collections = db['news_collection']
for item in news_list:
    collections.update_one({ '_id': { '$eq': item['_id']}}, item, upsert=True)