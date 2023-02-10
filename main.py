import os
import sys

import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import requests as requests

pygame.init()

toponym_coodrinates = input('Введите координаты: ').split(',')
zinit = float(input('Введите масштаб: (0.xx) '))

dct_resp = {}
lst_resp = []

map = 'map'
coordsxy = [coords_long, coords_lat] = toponym_coodrinates

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
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
os.remove(map_file)


def apply_value(coordsxy, cnt=0.1):
    global map
    value = dropdown.getSelected()
    if value == 'map':
        map = 'map'
    elif value == 'sat':
        map = 'sat'
    elif value == 'sat,skl':
        map = 'sat,skl'
    update_map(screen, coordsxy, cnt=cnt)


def update_map(screen, coordsxy, cnt=0.1):
    global map
    map_params = {
        "ll": ",".join(coordsxy),
        "spn": ','.join([str(cnt), str(cnt)]),
        "l": map
    }
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    os.remove(map_file)


dropdown = Dropdown(
    screen, 70, 10, 100, 50, name='Схема',
    choices=[
        'Cхема',
        'Спутник',
        'Гибрид',
    ],
    borderRadius=3, colour=pygame.Color('white'), values=['map', 'sat', 'sat,skl'], direction='down', textHAlign='left'
)

button = Button(
    screen, 10, 10, 50, 50, text='выбрать', fontSize=30,
    margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
    radius=5, onClick=lambda: apply_value(coordsxy, cnt=cnt), font=pygame.font.SysFont('calibri', 10),
    textVAlign='bottom'
)

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if cnt / 1.5 >= 0:
                    cnt /= 1.5
                    update_map(screen, coordsxy, cnt=cnt)
            if event.key == pygame.K_PAGEDOWN:
                if cnt * 1.5 >= 0:
                    cnt *= 1.5
                    update_map(screen, coordsxy, cnt=cnt)
            if event.key == pygame.K_DOWN:
                if (float(coords_lat) - cnt * 2 <= 90) and (float(coords_lat) - cnt * 2) >= -90:
                    coords_lat = str(float(coords_lat) - cnt * 2)
                    coordsxy = [coords_long, coords_lat]
                    update_map(screen, coordsxy, cnt=cnt)
            if event.key == pygame.K_UP:
                if (float(coords_lat) + cnt * 2 <= 90) and (float(coords_lat) + cnt * 2) >= -90:
                    coords_lat = str(float(coords_lat) + cnt * 2)
                    coordsxy = [coords_long, coords_lat]
                    update_map(screen, coordsxy, cnt=cnt)
            if event.key == pygame.K_LEFT:
                if float(coords_long) - cnt * 2 < 180 and float(coords_long) - cnt * 2 > -180:
                    coords_long = str(float(coords_long) - cnt * 2)
                    coordsxy = [coords_long, coords_lat]
                    update_map(screen, coordsxy, cnt=cnt)
            if event.key == pygame.K_RIGHT:
                if float(coords_long) + cnt * 2 < 180 and float(coords_long) + cnt * 2 > -180:
                    coords_long = str(float(coords_long) + cnt * 2)
                    coordsxy = [coords_long, coords_lat]
                    update_map(screen, coordsxy, cnt=cnt)
        pygame_widgets.update(events)
        pygame.display.update()
sys.exit()
