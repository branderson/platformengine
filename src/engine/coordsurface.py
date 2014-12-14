__author__ = 'brad'

import pygame
import math


class CoordinateSurface(pygame.Surface):
    coordinate_array = {}
    coordinate_width = 0
    coordinate_height = 0

    def __init__(self, rect, (coordinate_width, coordinate_height)):
        try:
            pygame.Surface.__init__(self, (rect.width, rect.height))
        except:
            pygame.Surface.__init__(self, (rect[0], rect[1]))

        self.coordinate_width = coordinate_width
        self.coordinate_height = coordinate_height

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

    # Convert screen coordinates to game coordinates
    def convert_to_surface_coordinates(self, (x_coordinate, y_coordinate)):
        if x_coordinate > self.get_width() or y_coordinate > self.get_height():
            print("Cannot  enter values greater than size of surface")
            return
        game_x_coordinate = (float(self.coordinate_width)/float(self.get_width()))*x_coordinate
        game_y_coordinate = (float(self.coordinate_height)/float(self.get_height()))*y_coordinate
        print(str(game_x_coordinate) + " " + str(game_y_coordinate))
        return game_x_coordinate, game_y_coordinate

    # Convert game coordinates to screen coordinates
    def convert_to_screen_coordinates(self, (x_coordinate, y_coordinate)):
        if x_coordinate > self.coordinate_width or y_coordinate > self.coordinate_height:
            print("Cannot  enter values greater than coordinate size of surface")
            return
        screen_x_coordinate = (float(self.get_width())/float(self.coordinate_width))*x_coordinate
        screen_y_coordinate = (float(self.get_height())/float(self.coordinate_height))*y_coordinate
        print(str(screen_x_coordinate) + " " + str(screen_y_coordinate))
        return screen_x_coordinate, screen_y_coordinate