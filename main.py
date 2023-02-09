import os
import sys

import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import requests as requests
from pygame_widgets.textbox import TextBox

pygame.init()

toponym_coodrinates = input('Введите координаты: ').split(',')
zinit = float(input('Введите масштаб: (0.xx) '))

dct_resp = {}
lst_resp = []

mapBASE = ('map', 'sat', 'sat,skl')
map = mapBASE[0]
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


def apply_value():
    global mapBASE, map
    value = dropdown.getSelected()
    if value == 'map':
        map = mapBASE[0]
    elif value == 'sat':
        map = mapBASE[1]
    elif value == 'sat,skl':
        map = mapBASE[2]
    update_map()


# активируется клавишей enter или кнопкой 'искать'
def output_text():
    global coords_lat, coords_long
    srk = textbox.getText()
    geo_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode" \
                  f"={srk}&format=json"
    resp = requests.get(geo_request)
    json_response = resp.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coords = [float(f) for f in toponym['Point']['pos'].split(' ')]
    coords_long = str(toponym_coords[0])
    coords_lat = str(toponym_coords[1])
    update_map(top_coords=toponym_coords)


def update_map(top_coords=None):
    global screen, coords_lat, coords_long, map, cnt
    if top_coords is not None:
        map_params = {
            "ll": ",".join([coords_long, coords_lat]),
            "spn": ','.join([str(cnt), str(cnt)]),
            "l": map,
            "pt": ','.join([str(top_coords[0]), str(top_coords[1]), 'pm2rdm'])
        }
    else:
        map_params = {
            "ll": ",".join([coords_long, coords_lat]),
            "spn": ','.join([str(cnt), str(cnt)]),
            "l": map
        }
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    os.remove(map_file)


dropdown = Dropdown(
    screen, 490, 10, 100, 30, name='Схема',
    choices=[
        'Cхема',
        'Спутник',
        'Гибрид',
    ],
    borderRadius=3, colour=pygame.Color('white'), values=['map', 'sat', 'sat,skl'], direction='down', textHAlign='left'
)

button = Button(
    screen, 410, 10, 75, 30, text='Выбрать', fontSize=30,
    margin=20, inactiveColour=(200, 0, 100), pressedColour=(0, 255, 0),
    radius=5, onClick=apply_value, font=pygame.font.SysFont('calibri', 18),
    textVAlign='center'
)

textbox = TextBox(screen, 90, 10, 200, 30, fontSize=20,
                  borderColour=(200, 0, 100), textColour=(0, 0, 0),
                  onSubmit=output_text, radius=10, borderThickness=1)

button2 = Button(
    screen, 10, 10, 75, 30, text='Искать', fontSize=30,
    margin=15, inactiveColour=(200, 0, 100), pressedColour=(0, 255, 0),
    radius=5, onClick=output_text, font=pygame.font.SysFont('calibri', 18),
    textVAlign='center'
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
                    update_map()
            if event.key == pygame.K_PAGEDOWN:
                if cnt * 1.5 >= 0:
                    cnt *= 1.5
                    update_map()
            if event.key == pygame.K_DOWN:
                if (float(coords_lat) - cnt * 2 <= 90) and (float(coords_lat) - cnt * 2) >= -90:
                    coords_lat = str(float(coords_lat) - cnt * 2)
                    update_map()
            if event.key == pygame.K_UP:
                if (float(coords_lat) + cnt * 2 <= 90) and (float(coords_lat) + cnt * 2) >= -90:
                    coords_lat = str(float(coords_lat) + cnt * 2)
                    update_map()
            if event.key == pygame.K_LEFT:
                if float(coords_long) - cnt * 2 < 180 and float(coords_long) - cnt * 2 > -180:
                    coords_long = str(float(coords_long) - cnt * 2)
                    update_map()
            if event.key == pygame.K_RIGHT:
                if float(coords_long) + cnt * 2 < 180 and float(coords_long) + cnt * 2 > -180:
                    coords_long = str(float(coords_long) + cnt * 2)
                    update_map()
    pygame_widgets.update(events)
    pygame.display.update()
sys.exit()
