__author__ = 'brad'
import sys
import pygame
import engine

from pygame.locals import *


def main():
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((640, 480))
    game_surface = engine.CoordinateSurface(screen.get_rect(), 10, 10)
    game_surface.fill((255, 255, 255))
    screen.blit(game_surface, screen.get_rect())

    while True:
        if not run_game():
            break


def run_game():
    sprite_group = None

    # Game loop
    while True:
        # Draw functions
        draw_game(sprite_group)

        # Event handling
        for event in pygame.event.get():
            handle_event(event)

        # Update display
        pygame.display.update()


def draw_game(sprite_group):
    return


def handle_event(event):
    # Quit the game
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    return

if __name__ == '__main__':
    main()
