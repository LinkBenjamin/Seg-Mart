import pygame
import config.globalvars
import segment.analytics as analytics

from config.env_vars import *
from config.files import get_full_path
from config.constants import *
from collections import Counter

class UI:
    def __init__(self):
        
        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(get_full_path("static", "TwilioSansMono-Regular.otf"),UI_FONT_SIZE)

        self.identity_rect = pygame.Rect(10,10,150,40)
        self.clicking = False

    def bagsummary(self):
        retval =  "Shopping Bag\n"
        retval += "------------\n"
        
        item_count = Counter(config.globalvars.shopping_bag)
        sorted_items = sorted(item_count.items(), key=lambda x:x[0])
        
        for item, count in sorted_items:
    
            nameStr = config.globalvars.game_items[item][3] + ": "

            retval += nameStr
            retval += str(count)
            retval += "\n"

        return retval

    def display(self, player):

        # Display the identity box
        id_surf = self.font.render("Identity: " + config.globalvars.identity,False,TEXT_COLOR)
        id_rect = id_surf.get_rect(topleft = (10,10))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, id_rect.inflate(10,10))
        self.display_surface.blit(id_surf, id_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, id_rect.inflate(10,10),3)

        # Display the interaction notification, if there is one
        if ' ' not in config.globalvars.object_interaction:
            if config.globalvars.object_interaction == 't':
                zn_surf = self.font.render("Press [space] to check out.",False,TEXT_COLOR)
            else:
                zn_surf = self.font.render("Press [space] to add a " + config.globalvars.game_items[config.globalvars.object_interaction][3] + " to your shopping bag.",False,TEXT_COLOR)
            
            zn_rect = zn_surf.get_rect(topleft = (10,40))
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, zn_rect.inflate(10,10)) 
            self.display_surface.blit(zn_surf, zn_rect)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, zn_rect.inflate(10,10),3)

        #Display the Shopping Bag
        sb_surf = self.font.render(self.bagsummary(), False, TEXT_COLOR)
        sb_rect = sb_surf.get_rect(topleft = (10, 70))
        sb_clear_button = pygame.draw.rect(self.display_surface, 'light blue', [150, 70, 100,30], 0, 5)
        sb_clear_text = self.font.render('Clear', True, 'black')
        self.display_surface.blit(sb_clear_text, (155,75))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, sb_rect.inflate(10,10)) 
        self.display_surface.blit(sb_surf, sb_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, sb_rect.inflate(10,10),3)

        if (sb_clear_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.clicking):
            self.clicking = True

            config.globalvars.shopping_bag.clear()

        if(not pygame.mouse.get_pressed()[0]):
            self.clicking = False