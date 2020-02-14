import sys
import requests
import pygame
import os


def change_spn(flag):
    global spn
    print(spn)
    if flag:
        spn = [spn[0] * 2, spn[1] * 2]
    else:
        spn = [spn[0] / 2, spn[1] / 2]


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
now = 0
while running:
    screen.blit(pic, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 281:
                change_spn(True)
                show_map()
            elif event.key == 280:
                change_spn(False)
                show_map()

    pygame.display.flip()
pygame.quit()
