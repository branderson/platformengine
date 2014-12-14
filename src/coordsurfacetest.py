__author__ = 'brad'

import pygame
import engine

pygame.init()

surface = engine.CoordinateSurface((100, 100), (5, 5))
surface.convert_to_surface_coordinates((20, 20))
surface.convert_to_surface_coordinates((40, 20))
surface.convert_to_surface_coordinates((40, 30))
surface.convert_to_surface_coordinates((100, 100))
surface.convert_to_surface_coordinates((0, 0))
surface.convert_to_surface_coordinates((10, 10))
surface.convert_to_surface_coordinates((25, 37))
surface.convert_to_screen_coordinates((5, 5))
surface.convert_to_screen_coordinates((1.5, 2.1))
surface.convert_to_screen_coordinates((0, 0))