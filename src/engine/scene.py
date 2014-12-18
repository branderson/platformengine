__author__ = 'brad'

import pygame
from coordsurface import CoordinateSurface


class Scene(object):
    coordinate_array = {}
    views = []

    def __init__(self, (view_width, view_height), (scene_width, scene_height), (view_x, view_y)):
        # self.views.append(CoordinateSurface(rect, (view_width, view_height)))
        self.scene_width = scene_width
        self.scene_height = scene_height
        self.view_x = view_x
        self.view_y = view_y
        self.view_rect = pygame.Rect((view_x, view_y), (view_width, view_height))

    def insert_object(self, game_object, (x_coordinate, y_coordinate)):
        if x_coordinate > self.scene_width or y_coordinate > self.scene_height:
            return False
        else:
            coordinate = (x_coordinate, y_coordinate)
            game_object.rect.x = x_coordinate
            game_object.rect.y = y_coordinate
            game_object.scale(self.views[0].x_scale, self.views[0].y_scale)

        if coordinate in self.coordinate_array:
            self.coordinate_array[coordinate].append(game_object)
        else:
            self.coordinate_array[coordinate] = [game_object]
        return True

    def insert_object_centered(self, game_object, (x_coordinate, y_coordinate)):
        game_object.rect.x = x_coordinate
        game_object.rect.y = y_coordinate
        game_object.scale(self.views[0].x_scale, self.views[0].y_scale)
        adjusted_x = x_coordinate - game_object.rect_scaled.centerx
        adjusted_y = y_coordinate - game_object.rect_scaled.centery
        self.insert_object(game_object, (adjusted_x, adjusted_y))

    # Searches for object in coordinate_array and removes it if it exits, or finds at position and removes one
    # or removes all at position
    def remove_object(self, game_object=None):  # , (x_coordinate, y_coordinate)=None):
        # if (x_coordinate, y_coordinate) is not None:
        #     coordinate = (x_coordinate, y_coordinate)
        #     del self.coordinate_array[coordinate]
        # else:
        for key in self.coordinate_array.keys():
            if self.views[0].check_position(game_object) is not None:
                self.views[0].remove_object(game_object)
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
            for game_object in self.coordinate_array.keys():
                if self.views[0].checkPosition(game_object) is not None:
                    self.views[0].remove_object(game_object)
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

    """def convert_to_view_coordinates(self, (x_coordinate, y_coordinate)):
        if x_coordinate > self.get_width() or y_coordinate > self.get_height():
            print("Cannot  enter values greater than size of surface")
            return
        game_x_coordinate = (float(self.coordinate_width)/float(self.get_width()))*x_coordinate
        game_y_coordinate = (float(self.coordinate_height)/float(self.get_height()))*y_coordinate
        # print(str(game_x_coordinate) + " " + str(game_y_coordinate))
        return game_x_coordinate, game_y_coordinate"""

    def update(self):
        # self.view_rect = pygame.Rect((self.views[0].
        self.views[0].clear()
        for key in self.coordinate_array.keys():
            for game_object in self.coordinate_array[key]:
                object_rect = pygame.Rect(game_object.rect.topleft, (game_object.rect_scaled.width,
                                                                     game_object.rect_scaled.height))
                """if game_object.rect_scaled.colliderect(self.view_rect):
                    print("Should be drawing")
                    # If views not empty
                    self.views[0].insert_object(game_object, (self.view_rect.x + game_object.rect_scaled.x,
                                                              self.view_rect.y + game_object.rect_scaled.y))"""
                # print(str(self.view_rect.x) + " " + str(game_object.rect_scaled.x))
                # print(str(self.view_rect.y) + " " + str(game_object.rect_scaled.y))

                # print(str(self.views[0].x_scale) + " " + str(self.views[0].y_scale))
                if self.view_rect.colliderect(object_rect):
                    self.views[0].insert_object(game_object, (game_object.rect_scaled.x - self.view_rect.x,
                                                              game_object.rect_scaled.y - self.view_rect.y))
        self.views[0].update()

    def update_screen_coordinates(self, (width, height)):
        pygame.Surface.__init__(self, (width, height))
        self.x_scale = self.views[0].get_width()/float(self.coordinate_width)
        self.y_scale = self.views[0].get_height()/float(self.coordinate_height)
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