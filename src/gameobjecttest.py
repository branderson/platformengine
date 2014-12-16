__author__ = 'brad'

import pygame
import engine
from pygame.locals import *

RESOURCE_DIR = '../resources/'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COORDINATE_WIDTH = 1600
COORDINATE_HEIGHT = 1200
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
surface = engine.CoordinateSurface((SCREEN_WIDTH, SCREEN_HEIGHT), (COORDINATE_WIDTH, COORDINATE_HEIGHT))
surface.fill((255, 255, 255))

# Create objects
test1 = engine.GameObject(RESOURCE_DIR + '124.jpg')
test2 = engine.GameObject(RESOURCE_DIR + '256.jpg')
surface.insert_object(test1, (0, 0))

while True:
    screen.fill((255, 255, 255))
    surface.update()
    screen.blit(surface, screen.get_rect())
    pygame.display.update()
    # Move stuff
    surface.increment_object(test1, (1, 1))
    if surface.check_position(test1)[0] > surface.coordinate_width:
        surface.move_object(test1, (0, surface.check_position(test1)[1]))
    if surface.check_position(test1)[1] > surface.coordinate_height:
        surface.move_object(test1, (surface.check_position(test1)[0], 0))
    print(str(test1.rect.x) + " " + str(test1.rect.y))