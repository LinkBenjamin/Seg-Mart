import pygame, sys

from config.constants import *
from app.views.title_screen import TitleScreen
from app.views.world import World

class Game:
    def __init__(self):
        #  Initialize pygame.  Set the window size and title. The default state is "TITLE_SCREEN" so we'll
        #  always open with the title screen.  Init the other variables needed.
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.gamestate = "TITLE_SCREEN"
        pygame.display.set_caption(GAME_NAME + " " + GAME_VERSION)
        self.clock = pygame.time.Clock()
        self.titlescreen = TitleScreen(self.screen)
        self.world = World()

    def run(self):
        while True:
            #  The game can be in one of 3 states:  You're on the title screen, you're in the world, or you're quitting.
            match self.gamestate:
                case "TITLE_SCREEN":
                    self.gamestate = self.titlescreen.handle_events()
                    self.titlescreen.render()
                case "WORLD":
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.gamestate = "QUIT"
                    self.screen.fill('black')
                    self.world.run()
                    pygame.display.update()
                    self.clock.tick(FPS)
                case "QUIT":
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()