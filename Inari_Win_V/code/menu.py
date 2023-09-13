import pygame
from settings import *


class Buttons(pygame.sprite.Sprite):
    def __init__(self, name, x_pos, y_pos, text_input, action,  width, height, statut, type , name2= None):
        self.display_surface = pygame.display.get_surface()
        self.police = pygame.font.Font(ui_pygame_font, ui_font_size)
        self.image = pygame.image.load(name)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.action = action
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = self.police.render(self.text_input, True, 'white')
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))
        self.statut = statut
        self.name = name
        self.name2 = name2
        self.type = type
        self.width = width
        self.height = height
        
    def update(self):
        self.display_surface.blit(self.image, self.rect)
        self.display_surface.blit(self.text, self.text_rect)


    def check_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return self.action
        
    
    def change_color (self, position):
        col = 'blue'
        if self.text_input == 'Épuisé':
            col = 'red'
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.police.render(self.text_input, True, col)
            self.display_surface.blit(self.text, self.text_rect)

            if self.type == 'menu_button' and self.name2 != None:
                self.image = pygame.image.load(self.name2)
                self.image = pygame.transform.scale(self.image, (self.width+ 25, self.height + 13))
                self.rect = self.image.get_rect(center=(self.x_pos+15, self.y_pos-15))
        else:
            self.text = self.police.render(self.text_input, True, 'white')
            self.display_surface.blit(self.text, self.text_rect)

            if self.type == 'menu_button' and self.name2 != None:
                self.image = pygame.image.load(self.name)
                self.image = pygame.transform.scale(self.image, (self.width-10, self.height-10))
                self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
    
    def change_statut(self):
        self.image = pygame.image.load(self.name2)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
