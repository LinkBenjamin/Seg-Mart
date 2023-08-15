import pygame, os

from config.files import get_full_path
from config.constants import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups, sprite_type, surface = pygame.Surface((TILESIZE,TILESIZE))):
        # Instantiate the class we're inheriting from (with groups)
        super().__init__(groups)
        # Define the image and the location of this tile on the drawing
        self.image = surface
        self.sprite_type = sprite_type
        self.rect = self.image.get_rect(topleft=position)