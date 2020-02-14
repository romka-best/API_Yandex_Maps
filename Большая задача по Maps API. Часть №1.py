# -*- coding: utf8 -*-
import sys
import requests
import pygame
import os

# Можно изменять:
spn = [0.5, 0.5]
coords = [37.1, 57.1]

maps_server = 'http://static-maps.yandex.ru/1.x/'
map_params = {
    'll': str(coords[0]) + ',' + str(coords[1]),
    'spn': str(spn[0]) + ',' + str(spn[1]),
    'l': 'map'}
response = requests.get(maps_server, params=map_params)
with open('map.png', 'wb') as f:
    f.write(response.content)
pic = pygame.image.load('map.png')
os.remove('map.png')
pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True
now = 0
while running:
    screen.blit(pic, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
