__author__ = 'brad'
import pygame


class GameObject(pygame.sprite.Sprite, object):
    layer = 0
    images = {}

    def __init__(self, filename=None, layer=0, masks=None):
        pygame.sprite.Sprite.__init__(self)

        if filename is None:
            self.image = pygame.Surface((0, 0))
        else:
            try:
                self.image = pygame.image.load(filename).convert_alpha()
            except:
                self.image = pygame.Surface((0, 0))
                print("The image failed to load")
        self.rect = self.image.get_rect()
        self.image_scaled = None
        self.rect_scaled = self.image.get_rect()
        self.rect_draw = self.image.get_rect()
        self.layer = layer
        self.masks = []
        self.images['image'] = self.image
        if masks is not None:
            for mask in masks:
                self.add_mask(mask)

    def add_mask(self, mask):
        self.masks.append(mask)

    def remove_mask(self, mask):
        if self.masks.count(mask) != 0:
            while self.masks.remove(mask):
                pass

    def add_image(self, surface, key):
        self.images[key] = surface

    def change_image(self, key):
        self.image = self.images[key]

    def remove_image(self, key):
        if key in self.images:
            del self.images[key]

    def destroy(self):
        self.__del__()
        return True

    def draw(self, surface, x_scale, y_scale, x, y):
        rect_scaled = pygame.Rect((x, y), (int(self.rect.width*x_scale), int(self.rect.height*y_scale)))
        surface.blit(pygame.transform.scale(self.image, (int(self.image.get_width()*x_scale),
                                                         int(self.image.get_height()*y_scale))), rect_scaled)

    def scale(self, x_scale, y_scale):
        self.image_scaled = pygame.transform.scale(self.image, (int(self.image.get_width()*x_scale),
                                                                int(self.image.get_height()*y_scale)))
        # self.rect_scaled.inflate_ip(-x_scale, -y_scale)
        self.rect = pygame.Rect(self.rect.topleft, (int(self.rect.width*x_scale), int(self.rect.height*y_scale)))
        # print(str(self.rect_scaled.x) + " " + str(self.rect_scaled.y))
        # pygame.quit()

    @staticmethod
    def tint(input_surface, (r, g, b, a)):
        surface = input_surface.copy()
        surface.lock()
        for x in range(0, surface.get_width() - 1):
            for y in range(0, surface.get_height() - 1):
                new_r = surface.get_at((x, y)).r + r
                if new_r > 255:
                    new_r = 255
                elif new_r < 0:
                    new_r = 0
                new_g = surface.get_at((x, y)).g + g
                if new_g > 255:
                    new_g = 255
                elif new_g < 0:
                    new_g = 0
                new_b = surface.get_at((x, y)).b + b
                if new_b > 255:
                    new_b = 255
                elif new_b < 0:
                    new_b = 0
                new_a = surface.get_at((x, y)).a + a
                if new_a > 255:
                    new_a = 255
                elif new_a < 0:
                    new_a = 0
                surface.set_at((x, y), (new_r, new_g, new_b, new_a))
        surface.unlock()
        return surface