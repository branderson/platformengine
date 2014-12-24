__author__ = 'brad'

import pygame


class CoordinateSurface(pygame.Surface):

    def __init__(self, rect, coordinate_size):
        # This part should be cleaned up
        """The CoordinateSurface is essentially a pygame Surface
        with a builtin secondary coordinate system, which operates
        irrespectively of the screen coordinates. It holds pointers
        to game objects and can manipulate those objects.
        :rtype : CoordinateSurface
        """
        try:
            pygame.Surface.__init__(self, (rect.width, rect.height), flags=pygame.SRCALPHA | pygame.HWSURFACE)
        except:
            pygame.Surface.__init__(self, (rect[0], rect[1]), flags=pygame.SRCALPHA | pygame.HWSURFACE)
        self.coordinate_array = {}
        self.layers = []
        self.x_scale = 1.
        self.y_scale = 1.
        self.active = True
        self.coordinate_width = coordinate_size[0]
        self.coordinate_height = coordinate_size[1]
        self.x_scale = self.get_width()/float(self.coordinate_width)
        self.y_scale = self.get_height()/float(self.coordinate_height)

    def insert_object(self, game_object, coordinate):
        # TODO: Make return false if object not added.
        if coordinate[0] > self.coordinate_width or coordinate[1] > self.coordinate_height:
            return False
        if coordinate in self.coordinate_array:
            self.coordinate_array[coordinate].append(game_object)
        else:
            self.coordinate_array[coordinate] = [game_object]
        if game_object.layer not in self.layers:
            self.layers.append(game_object.layer)
            self.layers.sort()
        return True

    def insert_object_centered(self, game_object, coordinate):
        # game_object.scale(self.x_scale, self.y_scale)
        adjusted_x = coordinate[0] - game_object.rect.centerx
        adjusted_y = coordinate[1] - game_object.rect.centery
        return self.insert_object(game_object, (adjusted_x, adjusted_y))

    def remove_object(self, game_object):
        # TODO: Extend to remove all at position
        remove_layer = True
        for key in self.coordinate_array.keys():
            for ob in self.coordinate_array[key]:
                if ob.layer == game_object.layer:
                    remove_layer = False
        if remove_layer:
            self.layers.remove(game_object.layer)
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
        for key in self.coordinate_array.keys():
            del self.coordinate_array[key]
        self.coordinate_array = {}
        self.layers = []

    def check_collision(self, coordinate):
        if coordinate in self.coordinate_array:
            return True
        else:
            return False

    # Returns a list of game objects at position
    def check_collision_objects(self, coordinate):
        if coordinate in self.coordinate_array:
            return self.coordinate_array[coordinate]
        else:
            return None

    def move_object(self, game_object, coordinate):
        position = self.check_position(game_object)
        # We're gonna need to refactor so that each coordinate is a list of objects
        if position is not None:
            if coordinate in self.coordinate_array:
                self.coordinate_array[coordinate].append(game_object)
            else:
                self.coordinate_array[coordinate] = [game_object]
            self.coordinate_array[position].remove(game_object)
            if len(self.coordinate_array[position]) == 0:
                del self.coordinate_array[position]
            return True
        else:
            return False

    def increment_object(self, game_object, increment):
        return self.move_object(game_object, (self.check_position(game_object)[0] + increment[0],
                                          self.check_position(game_object)[1] + increment[1]))

    def check_position(self, game_object):
        for key in self.coordinate_array.keys():
            if self.coordinate_array[key].count(game_object) > 0:
                return key
        return None

    # Convert screen coordinates to game coordinates
    def convert_to_surface_coordinates(self, coordinate):
        if coordinate[0] > self.get_width() or coordinate[1] > self.get_height():
            print("Cannot  enter values greater than size of surface")
            return
        game_x_coordinate = (float(self.coordinate_width)/float(self.get_width()))*coordinate[0]
        game_y_coordinate = (float(self.coordinate_height)/float(self.get_height()))*coordinate[1]
        return game_x_coordinate, game_y_coordinate

    # Convert game coordinates to screen coordinates
    def convert_to_screen_coordinates(self, coordinate):
        if coordinate[0] > self.coordinate_width or coordinate[1] > self.coordinate_height:
            print("Cannot  enter values greater than coordinate size of surface")
            return
        screen_x_coordinate = (float(self.get_width())/float(self.coordinate_width))*coordinate[0]
        screen_y_coordinate = (float(self.get_height())/float(self.coordinate_height))*coordinate[1]
        # print(str(screen_x_coordinate) + " " + str(screen_y_coordinate))
        return screen_x_coordinate, screen_y_coordinate

    def update(self, fill=None, masks=None):
        if self.active:
            if fill is None:
                self.fill((0, 0, 0, 0))
            else:
                self.fill(fill)

            for layer in self.layers:
                for key in self.coordinate_array.keys():
                    for game_object in self.coordinate_array[key]:
                        if game_object.layer == layer and game_object.visible:
                            if masks is None:
                                self.draw_object(game_object)
                            else:
                                draw_game_object = False
                                for mask in masks:
                                    if game_object.masks.count(mask) != 0:
                                        draw_game_object = True
                                if draw_game_object:
                                    self.draw_object(game_object)

    # Unusably slow. Don't use except for stills.
    def tint(self, (r, g, b, a)):
        # TODO: Draw colored surface over surface instead.
        self.lock()
        for x in range(0, self.get_width() - 1):
            for y in range(0, self.get_height() - 1):
                new_r = self.get_at((x, y)).r + r
                if new_r > 255:
                    new_r = 255
                elif new_r < 0:
                    new_r = 0
                new_g = self.get_at((x, y)).g + g
                if new_g > 255:
                    new_g = 255
                elif new_g < 0:
                    new_g = 0
                new_b = self.get_at((x, y)).b + b
                if new_b > 255:
                    new_b = 255
                elif new_b < 0:
                    new_b = 0
                new_a = self.get_at((x, y)).a + a
                if new_a > 255:
                    new_a = 255
                elif new_a < 0:
                    new_a = 0
                self.set_at((x, y), (new_r, new_g, new_b, new_a))
        self.unlock()

    def update_screen_coordinates(self, new_size):
        pygame.Surface.__init__(self, new_size, flags=pygame.SRCALPHA | pygame.HWSURFACE)
        self.x_scale = float(self.get_width())/float(self.coordinate_width)
        self.y_scale = float(self.get_height())/float(self.coordinate_height)

    def update_objects(self):
        pass

    # Deprecated
    def draw_object(self, game_object):
        x = self.convert_to_screen_coordinates(self.check_position(game_object))[0]
        y = self.convert_to_screen_coordinates(self.check_position(game_object))[1]
        game_object.draw(self, self.x_scale, self.y_scale, x, y)

    def draw(self):
        for key in self.coordinate_array.keys():
            pass