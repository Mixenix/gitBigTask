import sys
from io import BytesIO
import requests as requests
# Этот класс поможет нам сделать картинку из потока байт
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:



toponym_coodrinates = input('Введите координаты: ').split(',')
z = input('Введите масштаб: ')
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "z": z,
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы