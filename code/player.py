import pygame
from entity import Entity
from settings import *
from support import *

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, salle, vie, coin, gem, sound_volume):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/player/test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.salle = salle
        self.attack = pygame.mixer.Sound('../sounds/player/attack.mp3')
        self.sound_volume = sound_volume
        
        self.import_player_assets()
        self.status = 'right'
        self.coin = coin
        self.gem = gem
        self.can_get_input = True

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        
        self.damage = player_stats['damage']
        self.health = int(vie)
        self.speed = player_stats['speed']
        self.stamina = player_stats['stamina']
        
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 1000
        
        self.obstacle_sprites = obstacle_sprites
        
        
    def import_player_assets(self):
        charchter_path = '../graphics/player/'
        self.animations = {'right' : [], 'left' : [], 
                           'right_idle' : [], 'left_idle' : [],
                           'right_attack' : [], 'left_attack' : []}
        for animation in self.animations.keys():
            full_path = charchter_path + animation
            self.animations[animation] = import_folder(full_path)
                  
    def input(self):
        if not self.attacking and self.can_get_input:
            keys = pygame.key.get_pressed()
            
            #mouvements
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'right'
            elif keys[pygame.K_DOWN] :
                self.direction.y = 1
                self.status = 'left'
            else:
                self.direction.y = 0
                
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0
                
            #attaque
            if not self.attacking and self.stamina >= 60:
                if keys[pygame.K_SPACE]:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()    
                    self.attack.play()        
                    self.attack.set_volume(self.sound_volume/3)
                    if self.stamina - 60 < 0:
                        self.stamina = 0 
                    else:
                        self.stamina -= 60
    
    
        if self.direction.magnitude() !=0:
            self.direction= self.direction.normalize()
               
    def get_status(self):
        #idle statut
        if self.direction.x == 0 and  self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        #attaque statut
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in  self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
            
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        
        if self.frame_index  >= len(animation):
            self.get_status()
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        
        if not 'attack' in self.status:
            self.image = pygame.transform.scale(self.image, ( tile_size - 22, tile_size-5))
        else:
            self.image = pygame.transform.scale(self.image, (tile_size,tile_size- 10))
        self.rect = self.image.get_rect(center = self.hitbox.center)
        self.mask = pygame.mask.from_surface(self.image)
              
    def get_weapon_damage(self):
        return self.damage
              
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
            
    def update(self):
        self.input()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.speed)
        