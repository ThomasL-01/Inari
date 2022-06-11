import pygame
from settings import *
from menu import *

class UI: #Classe pour l'interface utilisateur
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(ui_font, ui_font_size)
        self.coeur = pygame.image.load('../graphics/player/health_bar.png').convert_alpha()
        self.coeur = pygame.transform.scale(self.coeur, (30,30))
        self.stamina = pygame.image.load('../graphics/stamina.png').convert_alpha()
        self.stamina = pygame.transform.scale(self.stamina, (40,40))
        self.ui_coin = True
        self.width, self.height = self.display_surface.get_size()
        self.val = 1
        self.button_list= []
        
        
        self.health_bar_rect = pygame.Rect(30,10,health_bar_width,bar_height) 
        self.boos_bar_rect = pygame.Rect(470, 37, 320, 17)
        self.stamina_bar_rect = pygame.Rect(40,40,stamina_bar_width,bar_height) 
        
        self.player_speech_image = pygame.image.load('../graphics/player_speech.png')
        self.player_speech_image = pygame.transform.scale(self.player_speech_image,(self.width , self.height / 2 + self.height /4))
        self.trader_speech_image = pygame.image.load('../graphics/trader_speech.png')
        self.trader_speech_image = pygame.transform.scale(self.trader_speech_image,(self.width, self.height / 2 + self.height /4))
        self.trade_menu_image = pygame.image.load('../graphics/Trade_menu.png')
        self.trade_menu_image = pygame.transform.scale(self.trade_menu_image, (self.width - self.width/10, self.height))

    #Fait apparaitre la barre de vie du joueur
    def show_bar(self,current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, '#242424', bg_rect)
        
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        
        pygame.draw.rect(self.display_surface, color, current_rect)    
        pygame.draw.rect(self.display_surface, 'black', bg_rect, 3)
    
    def show_stamina_bar(self,current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, '#242424', bg_rect)
        
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        if current < 130 and current > 58:
            color = '#00F021'
        elif current < 60 :
            color = 'orange'
        
        pygame.draw.rect(self.display_surface, color, current_rect)    
        pygame.draw.rect(self.display_surface, 'black', bg_rect, 3)
    
    #Fait apparaitre la barre de vie du boss
    def show_boss_bar(self, current, max_amount, bg_rect):
        boss_bar = pygame.image.load('../graphics/boss/boss_bar.png')
        boss_bar = pygame.transform.scale(boss_bar, (400, 30))
        
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        
        police = pygame.font.SysFont(ui_font, ui_font_size)
        texte = police.render('BOSS', 1 , 'red')
        self.display_surface.blit(texte, (600, 7))  
        self.display_surface.blit(boss_bar, (430,30))
        pygame.draw.rect(self.display_surface, 'red', current_rect)

    #Affiche l'inventaire de potions du joueur      
    def draw_potions(self, current_nb):
        height = self.display_surface.get_height()
        police = pygame.font.SysFont(ui_font, ui_font_size)
        texte = police.render(str(current_nb), 1 , 'white')
        self.image =  pygame.image.load('../graphics/autres/potion.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,60))
        if current_nb > 0:
            self.display_surface.blit(self.image, (60, height - 70))
            self.display_surface.blit(texte, (90, height - 25))

    def draw_keys(self, color, statut):
        height = self.display_surface.get_height()
        if color == 'red':
            self.image = pygame.image.load('../graphics/autres/cl_rouge.png')
        elif color == 'green':
            self.image = pygame.image.load('../graphics/autres/cl_verte.png')
        elif color == 'purp':
            self.image = pygame.image.load('../graphics/autres/cl_violette.png')
            
        self.image = pygame.transform.scale(self.image, (40,60))
            
        if statut == 'clé':
            self.display_surface.blit(self.image, (10, height - 70))
            
    def show_coins(self, current_nb, type):
        police = pygame.font.SysFont(ui_font, ui_font_size)
        texte = police.render(str(current_nb), 1 , 'white')
        if type == 'gem':
            self.image =  pygame.image.load('../graphics/gem/1.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (40,60))
            self.display_surface.blit(self.image, (140, 75))
            self.display_surface.blit(texte, (170, 115))
            
        elif type == 'coin':
            self.image =  pygame.image.load('../graphics/coin/5.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (40,60))
            self.display_surface.blit(self.image, (60, 75))
            self.display_surface.blit(texte, (90, 115))
    
    def player_speech(self):
        police = pygame.font.SysFont(ui_font, 33)
        self.display_surface.blit(self.player_speech_image, (0, self.height / 4))
        texte = police.render(speech[self.val], 1 , 'white')
        self.display_surface.blit(texte,(25, self.height - self.height / 6))
    
    def trader_speech(self):
        police = pygame.font.SysFont(ui_font, 33)
        self.display_surface.blit(self.trader_speech_image, (0, self.height / 4))
        texte = police.render(speech[self.val], 1 , 'white')
        self.display_surface.blit(texte,(25, self.height - self.height / 6))

    def trade_menu(self):
        self.display_surface.blit(self.trade_menu_image, (65, 0))
        market_button = '../graphics/autres/market_button.png'
        
        self.potion_button = Buttons(market_button, 400, 300, '20 gold', 'potion',170, 75,'ok','market_button','../graphics/autres/red_button.png' )
        
        self.strenght_button = Buttons(market_button, 575, 300, '5 gem', 'strenght',170, 75,'ok','market_button','../graphics/autres/red_button.png')
        
        self.stamina_button = Buttons(market_button, 740, 300, '5 gem', 'stamina',170, 75,'ok','market_button','../graphics/autres/red_button.png')
        
        self.health_button = Buttons(market_button, 915, 300, '10 gem', 'health',170, 75,'ok','market_button','../graphics/autres/red_button.png')
        
        self.speed_button = Buttons(market_button, 400, 600, '30 gold', 'speed',170, 75,'ok','market_button','../graphics/autres/red_button.png')
        
        self.resistance_button = Buttons(market_button, 575, 600, '15 gem', 'res',170, 75,'ok','market_button','../graphics/autres/red_button.png')
        
        self.close_button = Buttons('../graphics/autres/close_button.png', 950, 50, '', 'close', 75, 75, 'ok', 'market_button')
        
        self.button_list.extend([self.potion_button, self.stamina_button, self.strenght_button, self.speed_button, self.health_button, self.resistance_button ,self.close_button])
   
   
    #dessine la bar de vie
    def display(self, player):
        self.show_bar(player.health, player_stats['health'], self.health_bar_rect, 'red')
        self.show_stamina_bar(player.stamina, player_stats['stamina'], self.stamina_bar_rect, '#0000FF')
        self.display_surface.blit(self.coeur, (7,4))
        self.display_surface.blit(self.stamina, (7, 30))