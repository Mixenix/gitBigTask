import os
import sys

import pygame
import requests as requests

pygame.init()
toponym_coodrinates = input('Введите координаты: ').split(',')
zinit = float(input('Введите масштаб: (0.xx) '))
dct_resp = {}
lst_resp = []
coords_long, coords_lat = toponym_coodrinates
map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "ll": ",".join([coords_long, coords_lat]),
    "spn": ','.join([str(zinit), str(zinit)]),
    "l": "map"
}
response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
running = True
cnt = zinit
countleft = 1
countright = 1
countup = 1
countdown = 1
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
                if cnt / 1.5 >= 0 and cnt / 1.5 <= 90.0:
                    cnt /= 1.5
                    map_params = {
                        "ll": ",".join([coords_long, coords_lat]),
                        "spn": ','.join([str(cnt), str(cnt)]),
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
                if cnt * 1.5 >= 0 and cnt * 1.5 <= 90.0:
                    cnt *= 1.5
                    map_params = {
                        "ll": ",".join([coords_long, coords_lat]),
                        "spn": ','.join([str(cnt), str(cnt)]),
                        "l": "map"
                    }
                    response = requests.get(map_api_server, params=map_params)
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    screen.blit(pygame.image.load(map_file), (0, 0))
                    pygame.display.flip()
                    os.remove(map_file)
            if event.key == pygame.K_DOWN:
                if float(coords_lat) - cnt * 2 <= 180 and float(coords_lat) - cnt * 2 >= -180:
                    coords_lat = str(float(coords_lat) - cnt * 2)
                    map_params = {
                        "ll": ",".join([coords_long, coords_lat]),
                        "spn": ','.join([str(cnt), str(cnt)]),
                        "l": "map"
                    }
                    response = requests.get(map_api_server, params=map_params)
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    screen.blit(pygame.image.load(map_file), (0, 0))
                    pygame.display.flip()
                    os.remove(map_file)
            if event.key == pygame.K_UP:
                if float(coords_lat) + cnt * 2 <= 180 and float(coords_lat) + cnt * 2 >= -180:
                    coords_lat = str(float(coords_lat) + cnt * 2)
                    map_params = {
                        "ll": ",".join([coords_long, coords_lat]),
                        "spn": ','.join([str(cnt), str(cnt)]),
                        "l": "map"
                    }
                    response = requests.get(map_api_server, params=map_params)
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    screen.blit(pygame.image.load(map_file), (0, 0))
                    pygame.display.flip()
                    os.remove(map_file)
            if event.key == pygame.K_LEFT:
                if float(coords_long) - cnt * 2 <= 180 and float(coords_long) - cnt * 2 >= -180:
                    coords_long = str(float(coords_long) - cnt * 2)
                    map_params = {
                        "ll": ",".join([coords_long, coords_lat]),
                        "spn": ','.join([str(cnt), str(cnt)]),
                        "l": "map"
                    }
                    response = requests.get(map_api_server, params=map_params)
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    screen.blit(pygame.image.load(map_file), (0, 0))
                    pygame.display.flip()
                    os.remove(map_file)
            if event.key == pygame.K_RIGHT:
                if float(coords_long) + cnt * 2 <= 180 and float(coords_long) + cnt * 2 >= -180:
                    coords_long = str(float(coords_long) + cnt * 2)
                    map_params = {
                        "ll": ",".join([coords_long, coords_lat]),
                        "spn": ','.join([str(cnt), str(cnt)]),
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
