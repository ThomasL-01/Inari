import pygame
from settings import *
from entity import Entity
from support import *
from tile import Coin
from random import randint

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, visible_sprites, damage_player,coin_collision, salle, sound_volume):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        
        self.import_graphics(monster_name)
        self.salle = salle
        self.current_salle = salle
        self.death_sound_statut = True
        self.sound_volume = sound_volume

        self.coin = None
        self.can_get_coin = False
        self.gem = None
        self.has_spawned = False
        self.coin_cooldown_start = None
        self.coin_cooldown = 550
        self.coin_group = pygame.sprite.Group()
        self.no_coin = False
            
        self.death_animation_statut = True
        self.statut = 'left_idle'
        
        if monster_name == 'skeleton':
            self.image = pygame.image.load('../graphics/skeleton/right_idle/1.png')
        elif monster_name == 'boss':
            self.image = pygame.image.load('../graphics/boss/right_idle/1.png')

                      
        self.rect = self.image.get_rect(topleft = pos)
        if monster_name == 'skeleton':
            self.hitbox = self.rect.inflate(-10,-0)
        elif monster_name == 'boss':
            self.hitbox = self.rect.inflate(0,0)
            
        self.obstacle_sprites = obstacle_sprites
        self.visible_sprites = visible_sprites
        self.coin_collision = coin_collision
        
        self.monster_name = monster_name
        monster_info = mob_data[self.monster_name]
        self.health = monster_info['health']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.knockback = monster_info['knockback']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        
        self.vulnerable = True
        self.hit_time = None 
        self.invincibility_duration = 401

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        playerpos = player.rect.centerx
        enemypos = self.rect.centerx
        direction2 = playerpos - enemypos
            
        return (distance, direction, direction2)
      
    def import_graphics(self, name):
        self.animations = {'left_idle':[], 'left_move':[], 'left_attack':[], 'right_idle':[], 'right_move':[], 'right_attack':[], 'dead':[]}
        main_path = f'../graphics/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
            
    def get_statut(self, player):
        distance = self.get_player_distance_direction(player)[0]
        direction1 = self.get_player_distance_direction(player)[2]
        
        if distance <= self.attack_radius and self.can_attack == True:
            if self.statut != 'right_attack' and self.statut != 'left_attack':
                self.frame_index = 0
                if direction1 >= 0:
                    self.statut = 'right_attack'
                else:
                    self.statut = 'left_attack'
        elif distance <= self.notice_radius :
            if direction1 >= 0:
                self.statut = 'right_move'
            else:
                self.statut = 'left_move'
        else:
            self.statut = 'right_idle'
                    
    def actions(self,player):
        if self.statut == 'right_attack' or self.statut == 'left_attack' or self.statut == 'dead':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.statut)

        elif self.statut == 'right_move' or self.statut == 'left_move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
       
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
                
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
                
        if self.can_get_coin == False and self.statut == 'dead' and not self.no_coin:
            if current_time - self.coin_cooldown_start >= self.coin_cooldown:
                self.can_get_coin = True
            
        if self.salle == 14 or self.salle == 36:
            self.no_coin = True
        else:
            self.no_coin = False 
           
    def get_damage(self, player):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            self.health -=  player.get_weapon_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
              
    def check_death(self):
        if self.health <= 0:
            return True
                                  
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.knockback
                      
    def death_animation(self):
        self.statut = 'dead'
        self.coin_collision(self.coin_group, self.coin_cooldown_start)
        animation = self.animations[self.statut]  
        if self.death_animation_statut:
            self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = len(animation)-1
            self.death_animation_statut = False
            if self.coin is None and self.gem is None or self.monster_name == "boss":
                self.kill()

        self.image = animation[int(self.frame_index)]
        
        if self.monster_name == 'skeleton':
            self.image = pygame.transform.scale(self.image, (40,60))
            self.death_sound = pygame.mixer.Sound('../sounds/skeleton/death.mp3')
            
        if self.monster_name == 'boss':
            self.image = pygame.transform.scale(self.image, (100,140))
            self.death_sound = pygame.mixer.Sound('../sounds/boss/death.mp3')

        if self.death_sound_statut:
            self.death_sound.set_volume(self.sound_volume/2)
            self.death_sound.play()
            self.death_sound_statut = False
            self.frame_index = 0
                             
    def animate(self, monster_name):
        animation = self.animations[self.statut]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.statut == 'right_attack' :
                self.can_attack = False
            self.frame_index = 0
            if self.statut == 'left_attack':
                self.can_attack = False
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        
        if not 'attack' in self.statut:
            if monster_name == 'skeleton':
                self.image = pygame.transform.scale(self.image, (tile_size-10,tile_size))
            elif monster_name == 'boss':
                self.image = pygame.transform.scale(self.image, (tile_size+50,tile_size+90))
        else:
            if monster_name == 'skeleton':
                self.image = pygame.transform.scale(self.image, (tile_size,tile_size-10))
            elif monster_name == 'boss':
                self.image = pygame.transform.scale(self.image, (tile_size+ 50,tile_size+90))
                
        self.rect = self.image.get_rect(center = self.hitbox.center)
        self.mask = pygame.mask.from_surface(self.image)
        
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        
    def coin_update(self):
        coin_val = randint(1, 3)
        if coin_val == 1 and self.has_spawned == False:
            self.coin_cooldown_start = pygame.time.get_ticks()
            self.has_spawned = True
            self.gem = Coin([self.visible_sprites], (self.rect.x+ 10, self.rect.y + 20), self.current_salle, '../graphics/gem', "gem")
            self.gem.add(self.coin_group)
        elif coin_val > 1 and self.has_spawned == False:
            self.coin_cooldown_start = pygame.time.get_ticks()
            self.has_spawned = True
            self.coin = Coin([self.visible_sprites], (self.rect.x + 10, self.rect.y + 20), self.current_salle, '../graphics/coin', "coin")
            self.coin.add(self.coin_group)
    
    def update(self):
        if self.check_death() == True:
            self.death_animation()
        else:
            self.animate(self.monster_name)
            self.hit_reaction()
            self.move(self.speed)
                      
    def enemy_update(self, player):
        if self.check_death() != True:
            self.get_statut(player)
            self.actions(player)
        if self.check_death() and not self.no_coin:
            self.coin_update()
        self.cooldowns()