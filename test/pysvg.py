__author__ = 'brad'

import array
import math

import cairo
import pygame
import rsvg

WIDTH = 512
HEIGHT = 512

data = array.array('c', chr(0) * WIDTH * HEIGHT * 4)
surface = cairo.ImageSurface.create_for_data(
    data, cairo.FORMAT_ARGB32, WIDTH, HEIGHT, WIDTH * 4)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
svg = rsvg.Handle(file="../resources/NewTux.svg")
ctx = cairo.Context(surface)
svg.render_cairo(ctx)

image = pygame.image.frombuffer(data.tostring(), (WIDTH, HEIGHT),"ARGB")
screen.fill((255, 255, 255))
screen.blit(image, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()
while True:
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit