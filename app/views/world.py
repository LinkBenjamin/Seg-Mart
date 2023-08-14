import pygame

from config.tempMap import WORLD_MAP
from config.constants import *
from app.modules.tile import Tile
from app.modules.player import Player

class World:
    def __init__(self):

        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Create sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprites, self.obstacle_sprites])
                elif col == 'p':
                    self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        #Update and draw
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # Getting player offset for the camera
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)