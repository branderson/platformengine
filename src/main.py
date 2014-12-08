__author__ = 'brad'
import pygame
import engine


def main():
    pygame.init()

    # Set up the window
    display_surface = pygame.display.set_mode((640, 480))
    game_surface = engine.CoordinateSurface(display_surface.get_rect())
    game_surface.fill((0, 0, 0))
    display_surface.blit(game_surface, (0, 0))

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
    return

if __name__ == '__main__':
    main()
