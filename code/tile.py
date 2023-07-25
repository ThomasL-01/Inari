import pygame
from support import import_folder
from settings import *

#Toutes les classes pour les différents objets du décor
class Mur(pygame.sprite.Sprite):
    def __init__(self, pos, groups, name, salle):
        super().__init__(groups)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size,tile_size))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,0)
        self.salle = salle
            
class Vide_sol(pygame.sprite.Sprite):
    def __init__(self, groups, name, pos, salle):
        super().__init__(groups)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size,tile_size))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,0)
        self.salle = salle
        
class Porte(pygame.sprite.Sprite):
    def __init__(self, groups, name, pos, salle):
        super().__init__(groups)
        
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size,tile_size))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,0)
        self.salle = salle
        self.mask = pygame.mask.from_surface(self.image)
        
class Locked_porte_violette(pygame.sprite.Sprite):
    def __init__(self, groups, name, pos, statut, salle) -> None:
        super().__init__(groups)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size,tile_size))
        self.rect = self.image.get_rect(topleft = pos)
        self.statut = statut
        self.hitbox = self.rect.inflate(0,0)
        self.mask = pygame.mask.from_surface(self.image)
        self.salle = salle

class Locked_porte_verte(pygame.sprite.Sprite):
    def __init__(self, groups, name, pos, statut, salle) -> None:
        super().__init__(groups)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size,tile_size))
        self.rect = self.image.get_rect(topleft = pos)
        self.statut = statut
        self.hitbox = self.rect.inflate(0,0)
        self.mask = pygame.mask.from_surface(self.image)
        self.salle = salle

class Locked_porte_rouge(pygame.sprite.Sprite):
    def __init__(self, groups, name, pos, statut, salle) -> None:
        super().__init__(groups)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size,tile_size))
        self.rect = self.image.get_rect(topleft = pos)
        self.statut = statut
        self.hitbox = self.rect.inflate(0,0)
        self.mask = pygame.mask.from_surface(self.image)
        self.salle = salle
            
class Clé_verte(pygame.sprite.Sprite):
    def __init__(self, groups, name, pos, salle):
        super().__init__(groups)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size-20,tile_size-20))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,0)
        self.salle = salle
        
class Clé_rouge(pygame.sprite.Sprite):
    def __init__(self, groups, name, pos, salle):
        super().__init__(groups)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size-20,tile_size-20))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,0)
        self.salle = salle
        
class Clé_violette(pygame.sprite.Sprite):
    def __init__(self, groups, name, pos, salle):
        super().__init__(groups)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size-20,tile_size-20))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,0)
        self.salle = salle

class Lux(pygame.sprite.Sprite):
    def __init__(self, groups, pos, salle):
        super().__init__(*groups)
        self.image = pygame.image.load('../graphics/torch/1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (7,7))
        self.rect = self.image.get_rect(topleft = pos)
        self.salle = salle
        
        self.frame_index = 0
        self.animation_speed = 0.15
        self.folder = import_folder('../graphics/torch/')
        
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index  >= 7:
            self.frame_index = 0
        
        self.image = self.folder[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (tile_size-33,tile_size-12))

    def update(self):
        self.animate()
        
class Potion(pygame.sprite.Sprite):
    def __init__(self, groups, pos, salle):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/autres/potion.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size-30,tile_size-20))
        self.rect = self.image.get_rect(topleft = pos)
        self.salle = salle

class Coin(pygame.sprite.Sprite):
    def __init__(self, groups, pos, salle, name, type):
        super().__init__(groups)
        self.image = pygame.image.load(name+'/1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size-20,tile_size-20))
        self.rect = self.image.get_rect(topleft = pos)
        self.salle = salle
        self.type = type
        
        self.frame_index = 0
        self.animation_speed = 0.15
        self.folder = import_folder(name)
        
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index  >= 4:
            self.frame_index = 0
        
        self.image = self.folder[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (tile_size-25,tile_size-18))

    def update(self):
        self.animate()
        
class Trader(pygame.sprite.Sprite):
    def __init__(self, groups, pos, salle, visible_sprites):
        super().__init__(*groups)
        self.image = pygame.image.load('../graphics/traider/1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, ( tile_size - 22, tile_size-5))
        self.rect = self.image.get_rect(topleft = pos)
        self.display_surface = pygame.display.get_surface()
        self.salle = salle
        self.hitbox = self.rect.inflate(0,-10)
        self.radius = 15
        self.visible_sprites = visible_sprites
        self.speech = Speech( (self.rect.x, self.rect.y -25), self.salle)
        self.speech.add(self.visible_sprites)
        
        self.frame_index = 0
        self.animation_speed = 0.07
        self.folder = import_folder('../graphics/traider/')
        
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index  >= 7:
            self.frame_index = 0
        
        self.image = self.folder[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, ( tile_size - 22, tile_size))
        
    def update(self):
        self.animate()
        
class Speech(pygame.sprite.Sprite):
    def __init__(self, pos, salle):
        super().__init__()
        self.image = pygame.image.load('../graphics/speech/1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (7,7))
        self.rect = self.image.get_rect(topleft = pos)
        self.salle = salle
        
        self.frame_index = 0
        self.animation_speed = 0.075
        self.folder = import_folder('../graphics/speech/')
        
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index  >= 6:
            self.frame_index = 0
        
        self.image = self.folder[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (tile_size-20,tile_size-20))

    def update(self):
        self.animate()

    