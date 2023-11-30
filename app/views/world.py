import pygame, requests, config.globalvars, base64, json

from config.globalvars import game_items
from config.env_vars import *
from config.retailstore import *
from config.files import get_full_path
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

        self.impulse_item = 'q'
        self.worldrunning = False

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
                if '0' in val:
                    # This is an impulse-buy item, populated from the Segment profile.  
                    v = self.getfromSegmentprofile()
                else:
                    v = val
            
                if not ' ' in v:
                    image = pygame.image.load(get_full_path("static", "objects", str(game_items[v][0]) + ".png"))
                    Tile((j*TILESIZE, i*TILESIZE),game_items[v][1],[self.visible_sprites, self.items],v,image)

        # Load the player in the starting location.
        self.player = Player((320,256), -10, [self.visible_sprites], self.obstacle_sprites, self.items)

    def loadidentity(self,identity):
        self.identity = identity

    def run(self):
        if self.worldrunning:
            #Update and draw
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.update()
            self.ui.display(self.player)
        else:
            if 'nobody' not in config.globalvars.identity:
                self.worldrunning = True
                self.create_map()

    def getfromSegmentprofile(self):
        # 1 - get profile, find the trait we want (impulse_suggestion)
        # 1a - if the profile doesn't exist, return 'shoes'
        # 2 - this value can be 1-5. 1 = motor oil, 2 = laptop, 3 = shoes, 4 = plant, 5 = drink
        # 3 - return the associated letter code. 1 = o, 2 = q, 3 = v, 4 = p, 5 = r
        token_string = SEGMENT_API_TOKEN + ':'
        my_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(f"{SEGMENT_API_TOKEN}:".encode()).decode(),
            }
        req = SEGMENT_ENDPOINT.replace("<external_id>","user_id:"+ config.globalvars.identity)
        resp = requests.get(req,headers=my_headers)
        
        # if the profile doesn't have the trait, return shoes.
        
        if '[404]' in str(resp):
            rval = self.impulse_item
        else:
            # figure out which is the preferred object and return that
            if 'impulse_buy' in str(resp.content):
                # We got a response with 'impulse_buy' as an element.
                # This means that the profile exists and contains the
                # computed trait.
                x = json.loads(resp.content)
                print(x['traits']['impulse_buy'])
                match str(x['traits']['impulse_buy']):
                    case '1':
                        return 'o'
                    case '2':
                        return 'q'
                    case '3':
                        return 'v'
                    case '4':
                        return 'p'
                    case '5':
                        return 'r'
                    case _:
                        return 'r'
            else:
                # We didn't get a response with 'impulse_buy' as an element.
                # So either the profile doesn't exist, or it doesn't have the trait.
                # In this case, we put a default item on the impulse-buy shelf.
                return self.impulse_item
        return rval
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