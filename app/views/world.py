import pygame
import segment.analytics as analytics

from config.retailstore import *
from config.files import get_full_path
from config.globalvars import *
from config.constants import *
from app.modules.tile import Tile
from app.modules.player import Player
from app.modules.ui import UI

# This class creates the world and places the player in it.
# Currently there's only one world: 'retail store'.  But in the future
# all that would be necessary is to create a new .py file in /config that
# contains the arrays of items, and a .png file with the floor map on it
# to place behind the character, and you could add multiple worlds.
class World:
    def __init__(self):

        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Create sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.create_map()

        # UI
        self.ui = UI()

    def create_map(self):
        # Load (BARRIERS) - if anything is not blank, it's a barrier and we should load an obstacle tile
        for i in range(len(BARRIERS)):
            for j in range(len(BARRIERS[i])):
                if 'b' in BARRIERS[i][j]:
                    Tile((j * TILESIZE,i * TILESIZE),0,[self.obstacle_sprites],"barrier")

        # Load (DECORATIONS) - if anything is not blank, add it as an obstacle
        for i in range(len(DECORATIONS)):
            for j in range(len(DECORATIONS[i])):
                val = str(DECORATIONS[i][j])
                if not ' ' in val:
                    image = pygame.image.load(get_full_path("static", "objects", str(game_items[val][0]) + ".png"))
                    Tile((j*TILESIZE, i*TILESIZE),game_items[val][1],[self.visible_sprites, self.obstacle_sprites],game_items[val][2],image)

        # Load (ITEMS) - if anything is not blank, add it as interactable.
        for i in range(len(ITEMS)):
            for j in range(len(ITEMS[i])):
                val = str(ITEMS[i][j])
                if not ' ' in val:
                    image = pygame.image.load(get_full_path("static", "objects", str(game_items[val][0]) + ".png"))
                    Tile((j*TILESIZE, i*TILESIZE),game_items[val][1],[self.visible_sprites, self.items],val,image)

        # Load the player in the starting location.
        self.player = Player((320,256), -10, [self.visible_sprites], self.obstacle_sprites, self.items)

    def loadidentity(self,identity):
        self.identity = identity

    def run(self):
        #Update and draw
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)

# This Camera object detaches the viewscreen from the fixed position on the grid and
# allows us to track the player as they walk around the map.
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Create the floor
        self.floor_surf = pygame.image.load(get_full_path("static", BACKGROUND)).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

# custom_draw ensures that the camera tracks the player and ensures that the objects
# are stacked appropriately so that things "lower" on the grid appear in perspective relative
# to the viewer.
    def custom_draw(self, player):
        # Getting player offset for the camera
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Draw the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)