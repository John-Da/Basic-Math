import pygame
from game import Game

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Basic Math")
    done = False
    clock = pygame.time.Clock()
    game = Game()
    while not done:
        done = game.process_events()
        game.run_logic()
        game.power_up_button = game.add_power_up()
        game.show_hint_flag = False
        game.hint_start_time = 0
        game.display_frame(screen)
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()
