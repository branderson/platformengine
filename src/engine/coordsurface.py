__author__ = 'brad'

import pygame


class CoordinateSurface(pygame.Surface):
    coordinate_array = {}
    coordinate_width = 0
    coordinate_height = 0
    x_scale = 1.
    y_scale = 1.

    def __init__(self, rect, (coordinate_width, coordinate_height)):
        # This part should be cleaned up
        try:
            pygame.Surface.__init__(self, (rect.width, rect.height))
        except:
            pygame.Surface.__init__(self, (rect[0], rect[1]))

        self.coordinate_width = coordinate_width
        self.coordinate_height = coordinate_height
        self.x_scale = self.get_width()/float(coordinate_width)
        self.y_scale = self.get_height()/float(coordinate_height)

    def insert_object(self, game_object, (x_coordinate, y_coordinate)):
        if x_coordinate > self.coordinate_width or y_coordinate > self.coordinate_height:
            return False
        else:
            coordinate = (x_coordinate, y_coordinate)
            game_object.scale(self.x_scale, self.y_scale)

        if coordinate in self.coordinate_array:
            self.coordinate_array[coordinate].append(game_object)
        else:
            self.coordinate_array[coordinate] = [game_object]
        return True

    # Searches for object in coordinate_array and removes it if it exits, or finds at position and removes one
    # or removes all at position
    def remove_object(self, game_object=None):  # , (x_coordinate, y_coordinate)=None):
        # if (x_coordinate, y_coordinate) is not None:
        #     coordinate = (x_coordinate, y_coordinate)
        #     del self.coordinate_array[coordinate]
        # else:
        for key in self.coordinate_array.keys():
            if self.coordinate_array[key].count(game_object) > 0:
                self.coordinate_array[key].remove(game_object)
                if self.coordinate_array[key].__len__() == 0:
                    del self.coordinate_array[key]
                try:
                    game_object.delete()
                except:
                    pass
                return True
        return False

    def clear(self):
        # Delete the objects as well
        for key in self.coordinate_array.keys():
            del self.coordinate_array[key]

    def check_collision(self, (x_coordinate, y_coordinate)):
        coordinate = (x_coordinate, y_coordinate)
        if coordinate in self.coordinate_array:
            return True
        else:
            return False

    # Returns a list of game objects at position
    def check_collision_objects(self, (x_coordinate, y_coordinate)):
        coordinate = (x_coordinate, y_coordinate)
        if coordinate in self.coordinate_array:
            return self.coordinate_array[coordinate]
        else:
            return None

    def move_object(self, game_object, (x_destination, y_destination)):
        position = self.check_position(game_object)
        coordinate = (x_destination, y_destination)
        # We're gonna need to refactor so that each coordinate is a list of objects
        if position is not None:
            if coordinate in self.coordinate_array:
                self.coordinate_array[coordinate].append(game_object)
            else:
                self.coordinate_array[coordinate] = [game_object]
            self.coordinate_array[position].remove(game_object)
            if self.coordinate_array[position].__len__() == 0:
                del self.coordinate_array[position]
            return True
        else:
            return False

    def increment_object(self, game_object, (x_increment, y_increment)):
        if self.move_object(game_object, (self.check_position(game_object)[0] + x_increment,
                                          self.check_position(game_object)[1] + y_increment)):
            return True
        else:
            return False

    def check_position(self, game_object):
        for key in self.coordinate_array.keys():
            if self.coordinate_array[key].count(game_object) > 0:
                return key

    # Convert screen coordinates to game coordinates
    def convert_to_surface_coordinates(self, (x_coordinate, y_coordinate)):
        if x_coordinate > self.get_width() or y_coordinate > self.get_height():
            print("Cannot  enter values greater than size of surface")
            return
        game_x_coordinate = (float(self.coordinate_width)/float(self.get_width()))*x_coordinate
        game_y_coordinate = (float(self.coordinate_height)/float(self.get_height()))*y_coordinate
        # print(str(game_x_coordinate) + " " + str(game_y_coordinate))
        return game_x_coordinate, game_y_coordinate

    # Convert game coordinates to screen coordinates
    def convert_to_screen_coordinates(self, (x_coordinate, y_coordinate)):
        if x_coordinate > self.coordinate_width or y_coordinate > self.coordinate_height:
            print("Cannot  enter values greater than coordinate size of surface")
            return
        screen_x_coordinate = (float(self.get_width())/float(self.coordinate_width))*x_coordinate
        screen_y_coordinate = (float(self.get_height())/float(self.coordinate_height))*y_coordinate
        # print(str(screen_x_coordinate) + " " + str(screen_y_coordinate))
        return screen_x_coordinate, screen_y_coordinate

    def update(self):
        self.fill((255, 255, 255))
        for key in self.coordinate_array.keys():
            for game_object in self.coordinate_array[key]:
                game_object.rect_scaled.x = self.convert_to_screen_coordinates(self.check_position(game_object))[0]
                game_object.rect_scaled.y = self.convert_to_screen_coordinates(self.check_position(game_object))[1]
                # Possibly move draw to a separate function
                game_object.draw(self)
                # self.draw_object(game_object)

    def update_screen_coordinates(self, (width, height)):
        pygame.Surface.__init__(self, (width, height))
        self.x_scale = self.get_width()/float(self.coordinate_width)
        self.y_scale = self.get_height()/float(self.coordinate_height)
        for key in self.coordinate_array.keys():
            for game_object in self.coordinate_array[key]:
                game_object.scale(self.x_scale, self.y_scale)

    def update_objects(self):
        pass

    # Deprecated
    def draw_object(self, game_object):
        self.blit(pygame.transform.scale(game_object.image, (int(game_object.image.get_width()*self.x_scale),
                                                             int(game_object.image.get_height()*self.y_scale))),
                  game_object.rect.inflate(-self.x_scale, -self.y_scale))

    def draw(self):
        for key in self.coordinate_array.keys():
            pass