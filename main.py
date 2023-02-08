import sys
import os
import pygame
from io import BytesIO
import requests as requests
# Этот класс поможет нам сделать картинку из потока байт
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:


pygame.init()
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
lst_resp = []
map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
lst_resp.append(response)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(lst_resp[0].content)
running = True
cnt = 0
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            os.remove(map_file)
            sys.exit()
pygame.quit()
os.remove(map_file)
sys.exit()
