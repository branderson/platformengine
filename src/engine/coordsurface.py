__author__ = 'brad'

import pygame


class CoordinateSurface(pygame.Surface):
    coordinate_array = {}

    def __init__(self, rect, coordinate_width, coordinate_height):
        pygame.Surface.__init__(self, (rect.width, rect.height))

        # Initialize two dimensional list of pointers (consider using dictionary or numpy instead)
        coordinate_array = [[None for y in range(coordinate_height)] for x in range(coordinate_width)]