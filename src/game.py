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
CLOCK_SETTINGS = (TICKS_PER_SECOND, MAX_FPS, USE_WAIT, MAX_FRAME_SKIP, UPDATE_CALLBACK, FRAME_CALLBACK,
                  lambda: pygame.time.get_ticks()/1000.)
# Mask and string constants
RESOURCE_DIR = '../resources/'
GUI_MASK = ['gui']
GAME_MASK = ['game']


def main():
    global screen, game_state, game_surface1, game_surface2, background_surface, gui_surface, resource_manager, clock, \
        scene, current_width, player1_start, player2_start, current_state
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_state = engine.State()
    game_surface1 = engine.CoordinateSurface(pygame.Rect((0, 0),
                                                         (SCREEN_WIDTH, SCREEN_HEIGHT/2)),
                                             (COORDINATE_WIDTH, COORDINATE_HEIGHT/2))
    game_surface2 = engine.CoordinateSurface(pygame.Rect((0, SCREEN_HEIGHT/2),
                                                         (SCREEN_WIDTH, SCREEN_HEIGHT/2)),
                                             (COORDINATE_WIDTH, COORDINATE_HEIGHT/2))
    background_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)),
                                                  (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    gui_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT)),
                                           (COORDINATE_WIDTH/2, COORDINATE_HEIGHT))
    player1_start = (0, 0)
    player2_start = (300, 0)
    scene = engine.Scene((10000, 10000))
    game_state.add_scene('game', scene)
    current_state = game_state
    scene.insert_view(game_surface1, 'player1_view', player1_start, (0, 0), (255, 255, 255, 255))
    scene.insert_view(game_surface2, 'player2_view', player2_start, (0, SCREEN_HEIGHT/2), (255, 255, 255, 255))
    current_width = 800

    # Set up the clock
    clock = engine.GameClock(*CLOCK_SETTINGS)

    # Load the resources
    resource_manager = engine.ResourceManager()
    resource_manager.add_image('cat1', RESOURCE_DIR + '124.jpg')
    resource_manager.add_image('cat2', RESOURCE_DIR + '256.jpg')
    resource_manager.add_image('cat3', RESOURCE_DIR + '312.jpg')
    resource_manager.add_font('default', None, 12)

    while True:
        if not run_game():
            break


def run_game():
    global sprite_group, game_ticks, player1, player2
    sprite_group = pygame.sprite.Group()
    game_ticks = 0

    player1 = engine.GameObject(resource_manager.get_images('cat1'), 0)
    player2 = engine.GameObject(resource_manager.get_images('cat2'), -10)
    player3 = engine.GameObject(resource_manager.get_images('cat3'), -100)
    scene.insert_object_centered(player1, player1_start)
    scene.insert_object_centered(player2, player2_start)
    scene.insert_object_centered(player3, (COORDINATE_WIDTH/2, COORDINATE_HEIGHT/2))

    # Game loop
    while True:
        clock.tick()
        if clock.update_ready:
            update_clock()
            update_logic()

        if clock.frame_ready:
            # Draw functions
            draw_game()

            # Update display
            pygame.display.flip()

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
    current_state.update_collisions()
    if scene.check_object_collision(player1, player2):
        pygame.quit()
        sys.exit()
    key = pygame.key.get_pressed()
    if key[K_a]:
        player1.rotate(3)
    if key[K_d]:
        player1.rotate(-3)
    if key[K_s]:
        scene.increment_object_radial(player1, -3)
    if key[K_w]:
        scene.increment_object_radial(player1, 3)
    if key[K_LEFT]:
        player2.rotate(3)
    if key[K_RIGHT]:
        player2.rotate(-3)
    if key[K_UP]:
        scene.increment_object_radial(player2, 3)
    if key[K_DOWN]:
        scene.increment_object_radial(player2, -3)


def draw_game():
    scene.center_view_on_object('player1_view', player1)
    scene.center_view_on_object('player2_view', player2)
    current_state.update()
    background_surface.update((0, 0, 0, 255))
    gui_surface.update((0, 0, 0, 0))
    screen.blit(background_surface, (0, 0))
    for scene_key in current_state.scenes.keys():  # Draws each scene in the current state to the screen
        if current_state.scenes[scene_key].active:
            for surface_key in current_state.scenes[scene_key].views.keys():
                surface = current_state.scenes[scene_key].views[surface_key]
                if surface.active:
                    screen.blit(surface, current_state.scenes[scene_key].view_draw_positions[surface_key])
    screen.blit(gui_surface, (0, 0))
    pygame.draw.line(screen, (0, 0, 0, 255), (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2))
    return


def handle_event(event):
    # Quit the game
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    return


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()