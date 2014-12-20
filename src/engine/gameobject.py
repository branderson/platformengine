__author__ = 'brad'
import pygame


class GameObject(pygame.sprite.Sprite, object):
    layer = 0

    def __init__(self, filename=None, layer=0, masks=None):
        pygame.sprite.Sprite.__init__(self)

        if filename is None:
            self.image = pygame.Surface((0, 0))
        else:
            try:
                self.image = pygame.image.load(filename).convert()
            except:
                self.image = pygame.Surface((0, 0))
                print("The image failed to load")
        self.rect = self.image.get_rect()
        self.image_scaled = None
        self.rect_scaled = self.image.get_rect()
        self.rect_draw = self.image.get_rect()
        self.layer = layer
        self.masks = []
        if masks is not None:
            for mask in masks:
                self.add_mask(mask)

    def add_mask(self, mask):
        self.masks.append(mask)

    def remove_mask(self, mask):
        if self.masks.count(mask) != 0:
            while self.masks.remove(mask):
                pass

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
        self.rect_scaled = pygame.Rect(self.rect.topleft, (int(self.rect.width*x_scale), int(self.rect.height*y_scale)))
        # print(str(self.rect_scaled.x) + " " + str(self.rect_scaled.y))
        # pygame.quit()