import requests
import json

# 1. (Обязательное) Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев 
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

main_link = 'https://api.github.com/'
user = ('SergeyLazarevich')

link = f'{main_link}users/{user}/repos'

response = requests.get(link).json()

print('Список репозиториев:')
for repo in response:
    if not repo['private']:
        print(repo['html_url'])

with open('SergeyLazarevich.json','w', encoding='utf-8') as files:
            json.dump(response, files)

# 2.  (По желанию/возможности)Изучить список открытых API (https://www.programmableweb.com/category/all/apis). 
# Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. 
# Ответ сервера записать в файл.

def video_list(video):
    """ Get channel's upload videos| 50 limit"""

    YOUTUBE_API_KEY = 'AIzaSyDeYX4AGmuSrNb9Vp4dJbR5qbOIJxQsquU'

    # отрезаем id канала
    CHANNEL_ID = video.rsplit('/', 2)[-2]
    
    try:
        YOUTUBE_URI = f'https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=50'

        content = requests.get(YOUTUBE_URI).json()

        video_list =[]
        keys = 'id', 'title', 'description', 'preview'

        for item in content['items']:
            id = item['id']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            preview = item['snippet']['thumbnails']['high']['url']

            values = id, title, description, preview

            if id:
                video_item =dict(zip(keys, values))
                video_list.append(video_item)

        return video_list
    except:
        return {}

youtube_link = 'https://www.youtube.com/channel/UCQoTxtReDBqCYB_SVQO-Lpw/featured'
video_lists = video_list(youtube_link)

with open('Basic_Programming_vidio.json','w', encoding='utf-8') as files:
            json.dump(video_lists, files)