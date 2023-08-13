import pygame, sys

from config.constants import *
#from app.views.title_screen import TitleScreen
from app.views.world import World

class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.gamestate = "RUNNING"
        pygame.display.set_caption(GAME_NAME + " " + GAME_VERSION)
        self.clock = pygame.time.Clock()
 #       self.titlescreen = TitleScreen(self.screen)
        self.world = World()

    def run(self):
        while True:
            if self.gamestate == "TITLE_SCREEN":
                self.gamestate = self.titlescreen.handle_events()
                self.titlescreen.render()
            elif self.gamestate == "RUNNING":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                self.screen.fill('black')
                self.world.run()
                pygame.display.update()
                self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()