import pygame
from math import sin

class Entity(pygame.sprite.Sprite): #Classe "mère" des entités joueur et ennemi
    def __init__(self, groups ) :
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        
    #Création des collisions avec les hitbox des entités
    def collision(self, direction):
        if direction == 'horizontale':  #collision horizontale
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # deplacement à droite
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # deplacement à gauche
                        self.hitbox.left = sprite.hitbox.right
                        
        if direction == 'verticale':    #collision verticale
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # deplacement en bas
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # deplacement en haut
                        self.hitbox.top = sprite.hitbox.bottom
                        
    def move(self, speed):  #Fonction de mouvement des entités
        if self.direction.magnitude() !=0:
            self.direction= self.direction.normalize()
            
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontale')
        self.hitbox.y += self.direction.y * speed
        self.collision('verticale')
        self.rect.center = self.hitbox.center
        
    def wave_value(self):   #fonction pour faire "miroiter" l'entité lorsqu'elle prnds des dégats (avec fonction sin comme la derniere fois)
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0