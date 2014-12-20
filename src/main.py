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
GUI_MASK = ['gui']
GAME_MASK = ['game']


def main():
    global screen, game_surface, gui_surface, clock, scene, current_width, gui
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT)),
                                            (COORDINATE_WIDTH/2, COORDINATE_HEIGHT))
    gui_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT)),
                                           (COORDINATE_WIDTH/2, COORDINATE_HEIGHT))
    gui = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)),
                                            (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    scene = engine.Scene((10000, 10000))
    scene.insert_view(game_surface, (0, 0))
    scene.insert_view(gui_surface, (0, 0))
    scene.insert_view(gui, (0, 0))
    screen.blit(game_surface, (0, 0))
    screen.blit(gui_surface, (400, 0))
    screen.blit(gui, (0, 0))
    current_width = 800

    # Set up the clock
    clock = engine.GameClock(*CLOCK_SETTINGS)

    while True:
        if not run_game():
            break


def run_game():
    global screen, game_surface, gui_surface, sprite_group, game_ticks, clock, switched, scene, test1, test2, \
        gui
    sprite_group = pygame.sprite.Group()
    game_ticks = 0

    # Test code begin
    test1 = engine.GameObject(RESOURCE_DIR + '124.jpg', masks=['mask1'])
    scene.insert_object(test1, (75, 75))
    test2 = engine.GameObject(RESOURCE_DIR + '256.jpg', masks=['mask2'])
    scene.insert_object(test2, (175, 75))
    test3 = engine.GameObject(RESOURCE_DIR + '312.jpg', masks=['gui'])
    scene.insert_object(test3, (300, 0))
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
    global scene, test1, test2
    key = pygame.key.get_pressed()
    if key[K_a]:
        scene.pan_view((5, 0), 0)
    if key[K_d]:
        scene.pan_view((-5, 0), 0)
    if key[K_s]:
        scene.pan_view((0, -5), 0)
    if key[K_w]:
        scene.pan_view((0, 5), 0)
    if key[K_LEFT]:
        scene.increment_object(test1, (-5, 0))
    if key[K_RIGHT]:
        scene.increment_object(test1, (5, 0))
    if key[K_UP]:
        scene.increment_object(test1, (0, -5))
    if key[K_DOWN]:
        scene.increment_object(test1, (0, 5))


def draw_game():
    global sprite_group, game_surface, gui_surface, screen, scene, current_width, gui
    scene.update(0, masks=['mask1', 'mask2'])
    scene.update(1, masks=['mask2'])
    scene.update(2, (0, 0, 0, 0), ['mask1', 'gui'])
    # game_surface2.fill((125, 125, 125))
    # game_surface.draw()
    # sprite_group.draw(game_surface)
    screen.blit(game_surface, (0, 0))
    screen.blit(gui_surface, (current_width/2, 0))
    screen.blit(gui, (0, 0))
    return


def handle_event(event):
    global screen, game_surface, switched, scene, test1, current_width
    # Quit the game
    if event.type == QUIT:
        pygame.quit()
        sys.exit()

    # Test code begin
    if event.type == KEYUP:
        if event.key == K_q:
            if switched:
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                scene.update_screen_coordinates((SCREEN_WIDTH/2, SCREEN_HEIGHT), 0)
                scene.update_screen_coordinates((SCREEN_WIDTH/2, SCREEN_HEIGHT), 1)
                scene.update_screen_coordinates((SCREEN_WIDTH, SCREEN_HEIGHT), 2)
                current_width = SCREEN_WIDTH
                switched = False
            else:
                screen = pygame.display.set_mode((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                scene.update_screen_coordinates((SCREEN_WIDTH/4, SCREEN_HEIGHT/2), 0)
                scene.update_screen_coordinates((SCREEN_WIDTH/4, SCREEN_HEIGHT/2), 1)
                scene.update_screen_coordinates((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 2)
                # scene.remove_object(test1)
                current_width = SCREEN_WIDTH/2
                switched = True
    # Test code end
    return

if __name__ == '__main__':
    main()
