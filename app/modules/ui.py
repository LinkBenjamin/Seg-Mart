import pygame
import config.globalvars
from config.files import get_full_path
from config.constants import *

class UI:
    def __init__(self):
        
        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(get_full_path("static", "TwilioSansMono-Regular.otf"),UI_FONT_SIZE)

        self.identity_rect = pygame.Rect(10,10,150,40)

    def display(self, player):
        id_surf = self.font.render("Identity: " + config.globalvars.identity,False,TEXT_COLOR)
        id_rect = id_surf.get_rect(topleft = (10,10))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, id_rect.inflate(10,10))
        self.display_surface.blit(id_surf, id_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, id_rect.inflate(10,10),3)

        zn_surf = self.font.render("Currently in " + config.globalvars.currentzone,False,TEXT_COLOR)
        zn_rect = zn_surf.get_rect(topleft = (10,40))

        #if len(config.globalvars.currentzone) == 0:
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, zn_rect.inflate(10,10)) 
        self.display_surface.blit(zn_surf, zn_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, zn_rect.inflate(10,10),3)