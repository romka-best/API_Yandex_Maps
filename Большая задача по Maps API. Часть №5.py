# -*- coding: utf8 -*-
import sys
import requests
import pygame
import os


class Button:
    """Класс, который создаёт кнопки и пишет на них текст"""

    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length // len(text))
        my_font = pygame.font.Font(None, font_size)
        my_text = my_font.render(text, 1, text_color)
        surface.blit(my_text, ((x + length / 2) - my_text.get_width() / 2,
                               (y + height / 2) - my_text.get_height() / 2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):
        for i in range(1, 10):
            s = pygame.Surface((length + (i * 2), height + (i * 2)))
            s.fill(color)
            alpha = (255 / (i + 2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x - i, y - i, length + i, height + i), width)
            surface.blit(s, (x - i, y - i))
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        pygame.draw.rect(surface, (190, 190, 190), (x, y, length, height), 1)
        return surface

    def pressed(self, mouse):
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and \
                self.rect.topleft[1] < mouse[1] < self.rect.bottomright[1]:
            return True
        return False


def draw_buttons(obj, c1, c2, c3, x, y, length, height, width, text, text_c1, text_c2, text_c3):
    """Статический метод, который рисует кнопки"""
    obj.create_button(screen, (c1, c2, c3), x, y, length, height, width, text,
                      (text_c1, text_c2, text_c3))


def change_spn(flag):
    global spn
    if flag:
        spn = [spn[0] * 2, spn[1] * 2]
    else:
        spn = [spn[0] / 2, spn[1] / 2]


def change_coords(type):
    global coords
    if type == "U":
        coords = [coords[0], coords[1] + (1 / 10)]
    elif type == "L":
        coords = [coords[0] - (1 / 10), coords[1]]
    elif type == "D":
        coords = [coords[0], coords[1] - (1 / 10)]
    elif type == "R":
        coords = [coords[0] + (1 / 10), coords[1]]


def change_map():
    global type_map
    if type_map == "map":
        type_map = "sat"
    elif type_map == "sat":
        type_map = "skl"
    elif type_map == "skl":
        type_map = "map"


def geocode(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if response:
        json_response = response.json()
        features = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return features if features else None


def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return None, None
    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def get_ll_span(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)

    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])

    envelope = toponym["boundedBy"]["Envelope"]

    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")

    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    span = f"{dx},{dy}"

    return (ll, span)


def search(text):
    global coords
    coords[0], coords[1] = get_coordinates(text)


def show_map():
    global pic
    maps_server = 'http://static-maps.yandex.ru/1.x/'
    map_params = {
        'll': str(coords[0]) + ',' + str(coords[1]),
        'spn': str(spn[0]) + ',' + str(spn[1]),
        'l': type_map}
    response = requests.get(maps_server, params=map_params)
    with open('map.png', 'wb') as f:
        f.write(response.content)
    pic = pygame.image.load('map.png')
    os.remove('map.png')


spn = [0.5, 0.5]
coords = [37.1, 57.1]
type_map = "map"

pygame.init()
show_map()
screen = pygame.display.set_mode((600, 450))
running = True
search_button = Button()
search_text = " "
searching = False
now = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if searching:
                if event.unicode == "\x08":
                    search_text = search_text[:-1]
                elif event.unicode == "\r":
                    pass
                else:
                    search_text += event.unicode
            if event.key == 109 and not searching:  # Если нажимаем на M, то меняется тип карты
                change_map()
                show_map()
            elif event.key == 281:
                change_spn(True)
                show_map()
            elif event.key == 280:
                change_spn(False)
                show_map()
            elif event.key == 273:
                change_coords("U")
                show_map()
            elif event.key == 276:
                change_coords("L")
                show_map()
            elif event.key == 274:
                change_coords("D")
                show_map()
            elif event.key == 275:
                change_coords("R")
                show_map()
            elif event.key == 13:
                search(search_text)
                show_map()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if search_button.pressed(pygame.mouse.get_pos()):
                searching = True
            else:
                searching = False
    screen.blit(pic, (0, 0))
    try:  # Рисуем кнопки
        draw_buttons(search_button, 221, 221, 221, 0, 0, 600, 40, 0, search_text, 0, 0, 0)
    except ZeroDivisionError:  # но если пользователь нажал лишний раз <backspace>,
        # то не обращаем внимание на ошибку
        search_text = " "
    pygame.display.flip()
pygame.quit()
