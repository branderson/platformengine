__author__ = 'brad'

import pygame
import math
from coordsurface import CoordinateSurface


class Scene(object):
    coordinate_array = {}
    collision_array = {}
    views = {}
    view_rects = {}
    view_draw_positions = {}
    view_update_values = {}
    active = True

    def __init__(self, (scene_width, scene_height)):
        # self.views.append(CoordinateSurface(rect, (view_width, view_height)))
        self.scene_width = scene_width
        self.scene_height = scene_height

    def insert_view(self, surface, key, (view_x, view_y), view_draw_position=None, fill=None, masks=None,
                    view_size=None):
        if view_size is None:
            view_size = (surface.coordinate_width, surface.coordinate_height)
        self.views[key] = surface
        self.view_rects[key] = pygame.Rect((view_x, view_y), view_size)
        if view_draw_position is None:
            self.view_draw_positions[key] = (0, 0)
        else:
            self.view_draw_positions[key] = view_draw_position
        self.view_update_values[key] = (fill, masks)

    def remove_view(self, key):
        if key in self.views:
            del self.views[key]
            del self.view_rects[key]
            del self.view_draw_positions[key]
            del self.view_update_values[key]

    def pan_view(self, view_index, (x_increment, y_increment)):
        # May or may not need the scales here. Further testing is required
        self.view_rects[view_index].x += x_increment  # self.views[view_index].x_scale
        self.view_rects[view_index].y += y_increment  # *self.views[view_index].y_scale

    def move_view(self, key, (view_x, view_y)):
        self.view_rects[key].topleft = (view_x, view_y)

    # This one's a mathy doozy, but it centers the view on the object
    def center_view_on_object(self, key, game_object):
        self.view_rects[key] = pygame.Rect((self.check_position(game_object)[0] -
                                            self.view_rects[key].width/2 +
                                            game_object.rect.width/2,
                                            self.check_position(game_object)[1] -
                                            self.view_rects[key].height/2 + game_object.rect.height/2),
                                           (self.view_rects[key].width,
                                            self.view_rects[key].height))

    def insert_object(self, game_object, (x_coordinate, y_coordinate)):
        if x_coordinate > self.scene_width or y_coordinate > self.scene_height:
            return False
        else:
            coordinate = (x_coordinate, y_coordinate)
            # game_object.rect.x = x_coordinate
            # game_object.rect.y = y_coordinate

        if coordinate in self.coordinate_array:
            self.coordinate_array[coordinate].append(game_object)
        else:
            self.coordinate_array[coordinate] = [game_object]
        return True

    def insert_object_centered(self, game_object, (x_coordinate, y_coordinate)):
        # game_object.rect.x = x_coordinate
        # game_object.rect.y = y_coordinate
        # game_object.scale(self.views[view_index].x_scale, self.views[view_index].y_scale)
        adjusted_x = x_coordinate - game_object.rect.centerx
        adjusted_y = y_coordinate - game_object.rect.centery
        self.insert_object(game_object, (adjusted_x, adjusted_y))

    # Searches for object in coordinate_array and removes it if it exits, or finds at position and removes one
    # or removes all at position
    def remove_object(self, game_object=None):  # , (x_coordinate, y_coordinate)=None):
        # if (x_coordinate, y_coordinate) is not None:
        #     coordinate = (x_coordinate, y_coordinate)
        #     del self.coordinate_array[coordinate]
        # else:
        for key in self.coordinate_array.keys():
            for view in self.views.keys():
                if self.views[view].check_position(game_object) is not None:
                    self.views[view].remove_object(game_object)
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

    def clear(self, view_index=0):
        # Delete the objects as well
        for key in self.coordinate_array.keys():
            for game_object in self.coordinate_array.keys():
                if self.views[view_index].checkPosition(game_object) is not None:
                    self.views[view_index].remove_object(game_object)
            del self.coordinate_array[key]

    def check_collision(self, coordinate, game_object=None):
        """Checks if any object at position, or if game_object at position"""
        if game_object is None:
            for rect in self.collision_array.viewitems():
                if rect.collidepoint(coordinate):
                    return True
                else:
                    return False
        else:
            if game_object in self.collision_array:
                if self.collision_array[game_object].collidepoint(coordinate):
                    return True
            return False

    def check_collision_objects(self, coordinate):
        """Returns a list of game objects at position"""
        object_list = []
        for game_object in self.collision_array:
            if self.coordinate_array[game_object].collidepoint(coordinate):
                object_list.append(game_object)
        return object_list

    def check_object_collision(self, game_object1, game_object2):
        """Checks whether two objects collide"""
        if self.collision_array[game_object1].colliderect(self.collision_array[game_object2]):
            return True
        else:
            return False

    def move_object(self, game_object, (x_destination, y_destination)):
        position = self.check_position(game_object)
        coordinate = (x_destination, y_destination)
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

    def increment_object_radial(self, game_object, increment):
        x_increment = math.cos(math.radians(game_object.angle))*increment
        y_increment = math.sin(math.radians(game_object.angle))*increment
        if self.increment_object(game_object, (x_increment, y_increment)):
            return True
        else:
            return False

    def check_position(self, game_object):
        for key in self.coordinate_array.keys():
            if self.coordinate_array[key].count(game_object) > 0:
                return key

    def update(self, view_index=0, fill=None, masks=None):
        # self.view_rect = self.views[0].get_rect()
        self.views[view_index].clear()
        for key in self.coordinate_array.keys():
            for game_object in self.coordinate_array[key]:
                add_object = False
                object_rect = pygame.Rect(self.check_position(game_object), (game_object.rect.width,  # *self.views[view_index].x_scale,  #_scaled.width,
                                                                             game_object.rect.height))  # *self.views[view_index].y_scale))  # _scaled.height))
                self.collision_array[game_object] = object_rect
                if self.view_rects[view_index].colliderect(object_rect):
                    if masks is None:
                        add_object = True
                    else:
                        for mask in masks:
                            if game_object.masks.count(mask) != 0:
                                add_object = True
                    if add_object:
                        self.views[view_index].insert_object(game_object, (self.check_position(game_object)[0] -
                                                                           self.view_rects[view_index].x,
                                                                           self.check_position(game_object)[1] -
                                                                           self.view_rects[view_index].y))
        self.views[view_index].update(fill, masks)

    def update_collisions(self):
        self.collision_array = {}
        for key in self.coordinate_array.keys():
            for game_object in self.coordinate_array[key]:
                collide_rect = pygame.Rect((self.check_position(game_object)[0] + game_object.rect.width/2 -
                                            game_object.collision_rect.width/2, self.check_position(game_object)[1] +
                                            game_object.rect.height/2 - game_object.collision_rect.height/2),
                                           (game_object.collision_rect.width,
                                            game_object.collision_rect.height))
                self.collision_array[game_object] = collide_rect

    def update_screen_coordinates(self, view_index, (width, height)):
        self.views[view_index].update_screen_coordinates((width, height))
        # self.view_rects[0] = pygame.Rect((view_x, view_y), (view_width, view_height))
        # for key in self.coordinate_array.keys():
        #     for game_object in self.coordinate_array[key]:
        #         game_object.scale(self.views[view_index].x_scale, self.views[view_index].y_scale)

    def update_objects(self):
        for view in self.views:
            view.update_objects()