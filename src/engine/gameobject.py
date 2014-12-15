__author__ = 'brad'
import pygame


class GameObject(object, pygame.sprite.Sprite):
    layer = 0

    def __init__(self, layer=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(0, 0)
        self.rect = self.image.get_rect()
        self.layer = layer

    def destroy(self):
        self.__del__()
        return True

    def draw(self, surface):
        surface.blit(self.image, self.rect)