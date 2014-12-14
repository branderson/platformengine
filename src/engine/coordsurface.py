__author__ = 'brad'

import pygame


class CoordinateSurface(object, pygame.Surface):
    coordinate_array = {}
    coordinate_width = 0
    coordinate_height = 0

    def __init__(self, rect, coordinate_width, coordinate_height):
        pygame.Surface.__init__(self, (rect.width, rect.height))
        self.coordinate_width = coordinate_width
        self.coordinate_height = coordinate_height

        # Initialize two dimensional list of pointers (consider using dictionary or numpy instead)
        # coordinate_array = [[None for y in range(coordinate_height)] for x in range(coordinate_width)]

    def insert_object(self, game_object, (x_coordinate, y_coordinate)):
        if x_coordinate > self.coordinate_width or y_coordinate > self.coordinate_height:
            return 0
        else:
            self.coordinate_array[(x_coordinate, y_coordinate)] = game_object

    # Searches for object in coordinate_array and removes it if it exits, or removes at position
    def remove_object(self, (x_coordinate, y_coordinate)=None, game_object=None):
        if not (x_coordinate, y_coordinate) is None:
            self.coordinate_array[(x_coordinate, y_coordinate)] = None
        else:
            for key in self.coordinate_array.keys():
                if key == game_object:
                    self.coordinate_array[key] = None

    def check_collision(self, (x_coordinate, y_coordinate)):
        if not self.coordinate_array[(x_coordinate, y_coordinate)] is None:
            return True
        else:
            return False

    def move_object(self, game_object, (x_destination, y_destination)):
        position = self.check_position(game_object)
        # We're gonna need to refactor so that each coordinate is a list of objects
        if True:
            self.coordinate_array[(x_destination, y_destination)] = game_object
            self.coordinate_array[position] = None

    def check_position(self, game_object):
        for key in self.coordinate_array.keys():
            if key == game_object:
                return key