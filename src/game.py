__author__ = 'brad'

import sys
import pygame
import engine

from pygame.locals import *

# Screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COORDINATE_WIDTH = 800
COORDINATE_HEIGHT = 600
# Clock constants
TICKS_PER_SECOND = 60.0
MAX_FPS = 60
USE_WAIT = True
MAX_FRAME_SKIP = 5
UPDATE_CALLBACK = None
FRAME_CALLBACK = None
CLOCK_SETTINGS = (TICKS_PER_SECOND, MAX_FPS, USE_WAIT, MAX_FRAME_SKIP, UPDATE_CALLBACK, FRAME_CALLBACK, lambda: pygame.time.get_ticks()/1000.)
# Mask and string constants
RESOURCE_DIR = '../resources/'
GUI_MASK = ['gui']
GAME_MASK = ['game']


def main():
    global screen, game_surface, gui_surface, clock, scene, current_width, gui, resource_manager
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
    scene.insert_view(game_surface, 'game_surface', (0, 0))
    scene.insert_view(gui_surface, 'gui_surface', (0, 0))
    screen.blit(game_surface, (0, 0))
    screen.blit(gui_surface, (SCREEN_WIDTH/2, 0))
    screen.blit(gui, (0, 0))
    current_width = 800

    # Set up the clock
    clock = engine.GameClock(*CLOCK_SETTINGS)

    # Load the resources
    resource_manager = engine.ResourceManager()
    resource_manager.add_image('cat1', RESOURCE_DIR + '124.jpg')
    resource_manager.add_image('cat2', RESOURCE_DIR + '256.jpg')
    resource_manager.add_image('cat3', RESOURCE_DIR + '312.jpg')

    while True:
        if not run_game():
            break


def run_game():
    global screen, game_surface, gui_surface, sprite_group, game_ticks, clock, switched, scene, test1, test2, \
        gui, test3, resource_manager
    sprite_group = pygame.sprite.Group()
    game_ticks = 0

    # Test code begin
    test1 = engine.GameObject(resource_manager.get_images('cat1'), 0, masks=['mask1'])
    scene.insert_object(test1, (75, 75))
    test2 = engine.GameObject(resource_manager.get_images('cat2'), -10, masks=['mask2'])
    scene.insert_object(test2, (175, 75))
    test3 = engine.GameObject(resource_manager.get_images('cat3'), 20, masks=['gui'])
    test3.add_image('red_tint', test3.tint(test3.image, (125, 0, 0, 0)))
    gui.insert_object_centered(test3, (COORDINATE_WIDTH/2, COORDINATE_HEIGHT/2))
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
        pygame.display.set_caption("FPS: " + str(clock.fps))


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
    global scene, test1, test2, test3
    scene.update_collisions()
    if scene.check_object_collision(test1, test2):
        scene.increment_object(test2, (1, 1))
    key = pygame.key.get_pressed()
    if key[K_a]:
        scene.pan_view('game_surface', (3, 0))
    if key[K_d]:
        scene.pan_view('game_surface', (-3, 0))
    if key[K_s]:
        scene.pan_view('game_surface', (0, -3))
    if key[K_w]:
        scene.pan_view('game_surface', (0, 3))
    if key[K_LEFT]:
        scene.increment_object(test1, (-3, 0))
    if key[K_RIGHT]:
        scene.increment_object(test1, (3, 0))
    if key[K_UP]:
        scene.increment_object(test1, (0, -3))
    if key[K_DOWN]:
        scene.increment_object(test1, (0, 3))
    if key[K_r]:
        test3.rotate(3)
        # test3.rotate(test3.current_image, 3)
    if key[K_g]:
        test3.angle = 0
        test3.rotate(0)


def draw_game():
    global sprite_group, game_surface, gui_surface, screen, scene, current_width, gui
    screen.fill((255, 255, 255, 255))
    scene.update('game_surface', fill=(0, 0, 0, 0), masks=['mask1', 'mask2'])
    # game_surface.tint((125, 0, 0, 0))
    scene.center_view_on_object('gui_surface', test1)
    scene.update('gui_surface', fill=(0, 0, 0, 0), masks=['mask1', 'mask2'])
    gui.update((0, 0, 0, 0), ['gui'])
    # game_surface2.fill((125, 125, 125))
    # game_surface.draw()
    # sprite_group.draw(game_surface)
    screen.blit(gui, (0, 0))
    screen.blit(game_surface, (0, 0))
    screen.blit(gui_surface, (current_width/2, 0))
    return


def handle_event(event):
    global screen, game_surface, switched, scene, test1, current_width, test3
    # Quit the game
    if event.type == QUIT:
        pygame.quit()
        sys.exit()

    # Test code begin
    if event.type == KEYUP:
        if event.key == K_q:
            if switched:
                test3.change_image('image')
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                scene.update_screen_coordinates('game_surface', (SCREEN_WIDTH/2, SCREEN_HEIGHT))
                scene.update_screen_coordinates('gui_surface', (SCREEN_WIDTH/2, SCREEN_HEIGHT))
                gui.update_screen_coordinates((SCREEN_WIDTH, SCREEN_HEIGHT))
                current_width = SCREEN_WIDTH
                switched = False
            else:
                test3.change_image('red_tint')
                screen = pygame.display.set_mode((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                scene.update_screen_coordinates('game_surface', (SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
                scene.update_screen_coordinates('gui_surface', (SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
                gui.update_screen_coordinates((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                # scene.remove_object(test1)
                current_width = SCREEN_WIDTH/2
                switched = True
        elif event.key == K_f:
            test3.flip(1, 0)
        elif event.key == K_t:
            test3.rotate(45)
    # Test code end
    return

if __name__ == '__main__':
    main()