__author__ = 'brad'
import sys
import pygame
import engine

from pygame.locals import *

# Set up constants
# Clock constants
TICKS_PER_SECOND = 30.0
MAX_FPS = 0
USE_WAIT = True
MAX_FRAME_SKIP = 0
UPDATE_CALLBACK = None
FRAME_CALLBACK = None
USE_PREDICTION = True
CLOCK_SETTINGS = (TICKS_PER_SECOND, MAX_FPS, USE_WAIT, MAX_FRAME_SKIP, UPDATE_CALLBACK, FRAME_CALLBACK)


def main():
    global screen, game_surface, clock
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((640, 480))
    game_surface = engine.CoordinateSurface(screen.get_rect(), 10, 10)
    game_surface.fill((255, 255, 255))
    screen.blit(game_surface, screen.get_rect())

    # Set up the clock
    clock = engine.GameClock(*CLOCK_SETTINGS)

    while True:
        if not run_game():
            break


def run_game():
    global sprite_group, game_ticks
    sprite_group = None
    game_ticks = 0

    # Game loop
    while True:
        clock.tick()
        if clock.update_ready:
            update_clock()
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
        global game_ticks

        # sprite_group.clear(screen)  # , eraser_image)
        # sprite_group.update(USE_PREDICTION)
        # handle_collisions()
        game_ticks += 1
        if game_ticks >= clock.ticks_per_second:
            # set_caption()
            game_ticks = 0


def draw_game():
    # sprite_group.draw(screen)
    return


def handle_event(event):
    # Quit the game
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    return

if __name__ == '__main__':
    main()
