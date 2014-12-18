__author__ = 'brad'
import sys
import pygame
import engine

from pygame.locals import *

# Set up constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COORDINATE_WIDTH = 800
COORDINATE_HEIGHT = 600
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
    global screen, game_surface, clock, scene
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_surface = engine.CoordinateSurface(screen.get_rect(), (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    # game_surface.fill((255, 255, 255))
    # game_surface = engine.CoordinateSurface(pygame.Rect((20, 50), (100, 100)), (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    scene = engine.Scene((10000, 10000), (COORDINATE_WIDTH, COORDINATE_HEIGHT), (0, 0))
    scene.views.append(game_surface)
    screen.blit(game_surface, screen.get_rect())

    # Set up the clock
    clock = engine.GameClock(*CLOCK_SETTINGS)

    while True:
        if not run_game():
            break


def run_game():
    global screen, game_surface, sprite_group, game_ticks, clock, switched, scene, test1
    sprite_group = pygame.sprite.Group()
    game_ticks = 0

    # Test code begin
    test1 = engine.GameObject(RESOURCE_DIR + '124.jpg')
    scene.insert_object(test1, (75, 75))
    switched = False
    # Test code end

    # Game loop
    while True:
        clock.tick()
        if clock.update_ready:
            update_clock()
            update_logic()
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


def update_logic():
    global scene
    key = pygame.key.get_pressed()
    if key[K_a]:
        scene.pan_view(0, (5, 0))
    if key[K_d]:
        scene.pan_view(0, (-5, 0))
    if key[K_s]:
        scene.pan_view(0, (0, -5))
    if key[K_w]:
        scene.pan_view(0, (0, 5))

def draw_game():
    global sprite_group, game_surface, screen, scene
    scene.update()
    # game_surface.draw()
    # sprite_group.draw(game_surface)
    screen.blit(game_surface, screen.get_rect())
    return


def handle_event(event):
    global screen, game_surface, switched, scene, test1
    # Quit the game
    if event.type == QUIT:
        pygame.quit()
        sys.exit()

    # Test code begin
    if event.type == KEYUP:
        if event.key == K_q:
            if switched:
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                scene.update_screen_coordinates((SCREEN_WIDTH, SCREEN_HEIGHT))
                switched = False
            else:
                screen = pygame.display.set_mode((400, 300))
                scene.update_screen_coordinates((400, 300))
                # scene.remove_object(test1)
                switched = True
    # Test code end
    return

if __name__ == '__main__':
    main()
