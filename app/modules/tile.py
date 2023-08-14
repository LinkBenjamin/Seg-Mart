import pygame, os

from config.files import get_full_path
from config.constants import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        # Instantiate the class we're inheriting from (with groups)
        super().__init__(groups)
        # Define the image and the location of this tile on the drawing
        self.image = pygame.image.load(get_full_path('static', 'Jeff.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0,-10)