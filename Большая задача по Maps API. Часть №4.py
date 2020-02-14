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
        my_font = pygame.font.Font("font/Roboto-Black.ttf", font_size)
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


def change_map():
    global type_map
    if type_map == "map":
        type_map = "sat"
    elif type_map == "sat":
        type_map = "skl"
    elif type_map == "skl":
        type_map = "map"


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
# search_button =
now = 0
while running:
    screen.blit(pic, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 109:  # Если нажимаем на M, то меняется тип карты
                change_map()
                show_map()
    pygame.display.flip()
pygame.quit()
