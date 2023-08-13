import pygame

class World:
    def __init__(self):

        # Get the display surface
        self.display_surface = pygame.display.get_surface()
        
        # Create sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()


    def run(self):
        #Update and draw
        pass