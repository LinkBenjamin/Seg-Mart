import pygame
import pygame_gui
import config.globalvars

from pygame.rect import Rect
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from config.files import get_full_path
from config.constants import *
from app.utils.validation import is_valid_email


class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load(get_full_path("static", "TitleScreen.png"))
        self.manager = pygame_gui.UIManager((1200,800))
        self.text_input = UITextEntryLine(relative_rect=Rect(400,540,400,50), manager=self.manager)
        self.clock = pygame.time.Clock()
        
    
    def handle_events(self):
        retval = "TITLE_SCREEN"
        time_delta = self.clock.tick(60)/1000.0
        for event in pygame.event.get():
            #  If the user presses ESC, we want to quit the game.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    retval = "QUIT"
                    break

            #  Otherwise, we just want to wait until they've finished entering their text
            #  We detect this as an enter key press.
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.text_input:
                        #  If the user's email is valid, we can now consider this their identity
                        #  and allow them into the world.
                        if is_valid_email(event.text):
                            config.globalvars.identity = event.text 
                            retval = "WORLD"
            self.manager.process_events(event)
        self.manager.update(time_delta)

        return retval

    def render(self):
        self.screen.blit(self.background, (0,0))
        self.manager.draw_ui(self.screen)
        pygame.display.update()