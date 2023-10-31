import pygame
from pytmx.util_pygame import load_pygame
from app.utils.imports import import_csv_layout

from config.tempMap import WORLD_MAP
from config.files import get_full_path
from config.constants import *
from app.modules.tile import Tile
from app.modules.player import Player
from app.modules.ui import UI

class World:
    def __init__(self):

        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Create sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.zones = pygame.sprite.Group()
        self.hotspots = pygame.sprite.Group()

        self.create_map()

        # UI
        self.ui = UI()

    def create_map(self):
        tmx_data = load_pygame(get_full_path("static", "Map.tmx"))
        layouts = {
            'boundary': tmx_data.get_layer_by_name('Barriers'),
            'zones': tmx_data.get_layer_by_name('Zones'),
            'hotspots': tmx_data.get_layer_by_name('Hotspots')
        }
        csvlayouts = {
            'objects': import_csv_layout(get_full_path("static", "Map_Objects.csv")),
            'interactables': import_csv_layout(get_full_path("static","Map_Interactables.csv"))
        }

        # Map the zones (departments of the store)
        for obj in layouts['zones']:
            Tile((obj.x, obj.y), [self.zones], obj.name, pygame.Surface((obj.width, obj.height)))

        # Map the hotspots (if the user presses interact while overlapping a hotspot they'll add the item to their "shopping bag")
        for x,y,s in layouts['hotspots']:
            if(s != 0):
                Tile((x * TILESIZE, y * TILESIZE), [self.hotspots], str(s))

        # Build a series of invisible obstacle tiles based on the boundary layer - handles all the walls
        for x,y,s in layouts['boundary']:
            if(s != 0):
                Tile((x * TILESIZE,y * TILESIZE),[self.obstacle_sprites],"barrier")

        # Build the objects that appear in the game.
        for style, layout in csvlayouts.items():
                for row_index, row in enumerate(layout):
                    for col_index, col in enumerate(row):
                        if int(col) > 0:
                            image = pygame.image.load(get_full_path("static", "objects", col + ".png"))
                            Tile((col_index*TILESIZE, row_index*TILESIZE), [self.visible_sprites, self.obstacle_sprites], "object", image)

        self.player = Player((320,64), [self.visible_sprites], self.obstacle_sprites, self.zones, self.hotspots)

    def loadidentity(self,identity):
        self.identity = identity

    def run(self):
        #Update and draw
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Create the floor
        self.floor_surf = pygame.image.load(get_full_path("static", "Map.png")).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

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