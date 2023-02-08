import sys
import os
import pygame
import copy
from io import BytesIO
import requests as requests
# Этот класс поможет нам сделать картинку из потока байт
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:


pygame.init()
toponym_coodrinates = input('Введите координаты: ').split(',')
zinit = int(input('Введите масштаб: '))
# Долгота и широта:
dct_resp = {}
lst_resp = []
toponym_longitude, toponym_lattitude = toponym_coodrinates
map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "z": str(zinit),
    "l": "map"
}
response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
running = True
cnt = zinit
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
os.remove(map_file)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if cnt + 1 in range(0, 18):
                    cnt += 1
                    map_params = {
                        "ll": ",".join([toponym_longitude, toponym_lattitude]),
                        "z": str(cnt),
                        "l": "map"
                    }
                    response = requests.get(map_api_server, params=map_params)
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    screen.blit(pygame.image.load(map_file), (0, 0))
                    pygame.display.flip()
                    os.remove(map_file)
            if event.key == pygame.K_PAGEDOWN:
                if cnt - 1 in range(0, 18):
                    cnt -= 1
                    map_params = {
                        "ll": ",".join([toponym_longitude, toponym_lattitude]),
                        "z": str(cnt),
                        "l": "map"
                    }
                    response = requests.get(map_api_server, params=map_params)
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    screen.blit(pygame.image.load(map_file), (0, 0))
                    pygame.display.flip()
                    os.remove(map_file)
sys.exit()
