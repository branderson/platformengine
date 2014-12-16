__author__ = 'brad'
import pygame


class GameObject(pygame.sprite.Sprite, object):
    layer = 0

    def __init__(self, filename=None, layer=0):
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
        self.layer = layer

    def destroy(self):
        self.__del__()
        return True

    def draw(self, surface):
        surface.blit(self.image_scaled, self.rect_scaled)

    def scale(self, x_scale, y_scale):
        self.image_scaled = pygame.transform.scale(self.image, (int(self.image.get_width()*x_scale),
                                                                int(self.image.get_height()*y_scale)))
        self.rect_scaled.inflate(-x_scale, -y_scale)