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
points = []

address = None
font = pygame.font.Font('freesansbold.ttf', 12)
mapBASE = ('map', 'sat', 'sat,skl')
map = mapBASE[0]
coords_long, coords_lat = toponym_coodrinates


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
    global coords_lat, coords_long, points, address
    srk = textbox.getText()
    if srk != '':
        geo_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode" \
                      f"={srk}&format=json"
        resp = requests.get(geo_request)
        json_response = resp.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coords = [float(f) for f in toponym['Point']['pos'].split(' ')]
        address = toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
        coords_long = str(toponym_coords[0])
        coords_lat = str(toponym_coords[1])

        points.append((','.join([str(toponym_coords[0]), str(toponym_coords[1]), 'pm2rdm']), address))
        update_map()


def address_print(address=None):
    global font
    if address is not None:
        text = font.render(address, True, (255, 0, 0))
    else:
        text = font.render('Адрес не задан', True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.x = 70
    textRect.y = 420
    screen.blit(text, textRect)


def reset():
    global points, address
    points = []
    address = None
    update_map()


def update_map():
    global screen, coords_lat, coords_long, map, cnt, address
    if len(points) > 0:
        map_params = {
            "ll": ",".join([coords_long, coords_lat]),
            "spn": ','.join([str(cnt), str(cnt)]),
            "l": map,
            "pt": ','.join(['~'.join([f[0] for f in points])])
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
    address_print(address)


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
address_print()
pygame.display.flip()
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

textbox = TextBox(screen, 90, 10, 200, 30, fontSize=20,
                  borderColour=(200, 0, 100), textColour=(0, 0, 0),
                  onSubmit=output_text, radius=10, borderThickness=1)

button_select = Button(
    screen, 410, 10, 75, 30, text='Выбрать', fontSize=30,
    margin=20, inactiveColour=(200, 0, 100), pressedColour=(0, 255, 0),
    radius=5, onClick=apply_value, font=pygame.font.SysFont('calibri', 18),
    textVAlign='center'
)

button_search = Button(
    screen, 10, 10, 75, 30, text='Искать', fontSize=30,
    margin=15, inactiveColour=(200, 0, 100), pressedColour=(0, 255, 0),
    radius=5, onClick=output_text, font=pygame.font.SysFont('calibri', 18),
    textVAlign='center'
)

button_reset = Button(
    screen, 10, 410, 50, 30, text='Сброс', fontSize=30,
    margin=15, inactiveColour=(200, 0, 100), pressedColour=(0, 255, 0),
    radius=5, onClick=reset, font=pygame.font.SysFont('calibri', 18),
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
