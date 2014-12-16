__author__ = 'brad'
import sys
import pygame
import engine

from pygame.locals import *

# Set up constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COORDINATE_WIDTH = 1600
COORDINATE_HEIGHT = 1200
# Clock constants
TICKS_PER_SECOND = 30.0
MAX_FPS = 0
USE_WAIT = True
MAX_FRAME_SKIP = 0
UPDATE_CALLBACK = None
FRAME_CALLBACK = None
CLOCK_SETTINGS = (TICKS_PER_SECOND, MAX_FPS, USE_WAIT, MAX_FRAME_SKIP, UPDATE_CALLBACK, FRAME_CALLBACK)
RESOURCE_DIR = '../resources/'


def main():
    global screen, game_surface, clock
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_surface = engine.CoordinateSurface(screen.get_rect(), (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    game_surface.fill((255, 255, 255))
    screen.blit(game_surface, screen.get_rect())

    # Set up the clock
    clock = engine.GameClock(*CLOCK_SETTINGS)

    while True:
        if not run_game():
            break


def run_game():
    global screen, game_surface, sprite_group, game_ticks, clock
    sprite_group = pygame.sprite.Group()
    game_ticks = 0

    # Game loop
    while True:
        clock.tick()
        if clock.update_ready:
            update_clock()
            game_surface.update_objects()

        if clock.frame_ready:
            # Draw functions
            draw_game()

            # Update display
            pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            handle_event(event)


def update_clock():
        """Update function for use with GameClock."""
        global game_ticks, clock

        # sprite_group.clear(screen)  # , eraser_image)
        # sprite_group.update(USE_PREDICTION)
        # handle_collisions()
        game_ticks += 1
        if game_ticks >= clock.ticks_per_second:
            # set_caption()
            game_ticks = 0


def draw_game():
    global sprite_group, game_surface, screen
    game_surface.update()
    # game_surface.draw()
    # sprite_group.draw(game_surface)
    screen.blit(game_surface, screen.get_rect())
    return


def handle_event(event):
    # Quit the game
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    return

if __name__ == '__main__':
    main()
