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
surface.insert_object('object', (5, 5))
surface.insert_object('object2', (5, 5))
print("Is there a collision? " + str(surface.check_collision((5, 5))))
print("The collision is with: " + surface.check_collision_objects((5, 5))[0] + " " +
      surface.check_collision_objects((5, 5))[1])
surface.move_object('object', (3, 4))
surface.remove_object('object2')
print("Where is object? " + str(surface.check_position('object')))
print("Is it really there? " + str(surface.check_collision_objects(surface.check_position('object'))))
print("What about object2? " + str(surface.check_collision((5, 5))))
surface.remove_object('object')
# Test delete/move until false
for i in xrange(1, 10):
    surface.insert_object('object', (1, 1))
while surface.remove_object('object'):
    print("Removed object")